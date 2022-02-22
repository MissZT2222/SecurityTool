#!/usr/bin/python3
# -*- coding: utf-8 -*-
from socket import *
import threading
import argparse
#线程锁
lock = threading.Lock()
openNum = 0
threads = []

def portScanner(host,port):
#定义全局变量
    global openNum
    try:
        s = socket(AF_INET,SOCK_STREAM)
        s.connect((host,port))
# 当多个线程同时执行lock.acquire()时,只有一个线程能成功地获取锁,然后继续执行代码,其他线程就继续等待直到获得锁为止
        lock.acquire()
        openNum+=1
        print('[+] %d open' % port)
#释放线程锁
        lock.release()
        #关闭网络连接
        s.close()
    except:
        pass

def main():
#argparse 模块可以让人轻松编写用户友好的命令行接口。程序定义它需要的参数，然后 argparse 将弄清如何从 sys.argv 解析出那些参数。 argparse 模块还会自动生成帮助和使用手册，并在用户给程序传入无效参数时报出错误信息。
    p = argparse.ArgumentParser(description='Port scanner!.')
    p.add_argument('-H', dest='hosts', type=str)
    args = p.parse_args()
    hostList = args.hosts.split(',')
    setdefaulttimeout(1)
    for host in hostList:
        print('Scanning the host:%s......' % (host))
 #给多线程传入扫描参数
        for p in range(1,1024):
            t = threading.Thread(target=portScanner,args=(host,p))
            threads.append(t)
            t.start()   
                
#阻塞当前进程/线程，直到调用join方法的那个进程执行完，再继续执行当前进程。
#join方法在java中即守护线程的概念：如果用户线程已经全部退出运行了，只剩下守护线程存在了，虚拟机也就退出了。 因为没有了被守护者，守护线程也就没有工作可做了，也就没有继续运行程序的必要了。
        for t in threads:
            t.join()

        print('[*] The host:%s scan is complete!' % (host))
        print('[*] A total of %d open port ' % (openNum))

if __name__ == '__main__':
    main()