#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import threading,time
import sys
from scapy.all import *


def get_ip():
    '''从命令行参数中获取 IP'''
    try:
        parameter = sys.argv
        ip = parameter[1]
        print('The IP you test is : ', end = '')
        print(ip)
    except Exception as e:
        print(e)
    return ip


def port_scan(port):
    '''扫描端口'''
    try:
        packet = IP(dst=ip)/TCP(dport=port,flags='S')   # 构造一个 flags 的值为 S 的报文
        send = sr1(packet,timeout=2,verbose=0)
        if send.haslayer('TCP'):   #发送报文并返回所有响应报文
            if send['TCP'].flags == 'SA':   # 判断目标主机是否返回 SYN+ACK
                send_1 = sr1(IP(dst=ip)/TCP(dport=port,flags='R'),timeout=2,verbose=0) # 只向目标主机发送 RST
                print('[+] %d is open' % port)
            elif send['TCP'].flags == 'RA':
                pass
    except:
        pass

def main():
    threads = []
    threads_count = 100     # 线程数，默认 100 个线程

    packet_ping = IP(dst=ip)/ICMP()     # 在扫描端口之前先用 ICMP 协议探测一下主机是否存活
    ping = sr1(packet_ping,timeout=2,verbose=0)
    if ping is not None:
        for p in range(1,1001):   # 默认扫描1-1000的端口，可以手动修改这里的端口范围
            t = threading.Thread(target=port_scan,args=(p,))
            threads.append(t)

        for t in threads:
            t.start()

        for t in threads:
            t.join()
    elif ping is None:
        print('该主机处于关闭状态或本机被该主机过滤，无法对其使用 ping 探测')


if __name__ == '__main__':
    ip = get_ip()
    start_time = time.time()
    main()
    end_time = time.time()
    print('[time cost] : ' + str(end_time-start_time) + ' 秒')