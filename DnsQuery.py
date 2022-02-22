#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import Queue
import sys
import dns.resolver
import threading
import time
import optparse
import os



class DnsQuery:
    def __init__(self, target, names_file, ignore_intranet, threads_num, output):
#strip() 方法用于移除字符串头尾指定的字符（默认为空格或换行符）或字符序列。
#target 值为传入的域名
        self.target = target.strip()
        #字典文件
        self.names_file = names_file
        self.ignore_intranet = ignore_intranet
        #线程数
        self.thread_count = self.threads_num = threads_num
        self.scan_count = self.found_count = 0
        #定义一个锁
        self.lock = threading.Lock()
        #DNS查询结果返回值
        self.resolvers = [dns.resolver.Resolver() for _ in range(threads_num)]
        self._load_dns_servers()
        self._load_sub_names()
        self._load_next_sub()
		#把扫描结果输出到一个文件中去
        outfile = target + '.txt' if not output else output
        self.outfile = open(outfile, 'w')   # won't close manually
        self.ip_dict = {}
        self.STOP_ME = False
		#传入DNS文件中的DNS服务器
    def _load_dns_servers(self):
        dns_servers = []
        with open('dict/dns_servers.txt') as f:
            for line in f:
                server = line.strip()
                if server.count('.') == 3 and server not in dns_servers:
                    dns_servers.append(server)
        self.dns_servers = dns_servers
        self.dns_count = len(dns_servers)
		#传入域名爆破字典中的值
    def _load_sub_names(self):
        self.queue = Queue.Queue()
        file = 'dict/' + self.names_file if not os.path.exists(self.names_file) else self.names_file
        with open(file) as f:
            for line in f:
                sub = line.strip()
                if sub: self.queue.put(sub)
	#传入字典，
    def _load_next_sub(self):
        next_subs = []
        with open('dict/next_sub.txt') as f:
            for line in f:
                sub = line.strip()
                if sub and sub not in next_subs:
                    next_subs.append(sub)
        self.next_subs = next_subs

    def _update_scan_count(self):
        self.lock.acquire()
        self.scan_count += 1
        self.lock.release()

    def _print_progress(self):
        self.lock.acquire()
        msg = '%s found | %s remaining | %s scanned in %.2f seconds' % (
            self.found_count, self.queue.qsize(), self.scan_count, time.time() - self.start_time)
			sys.stdout.flush()
        self.lock.release()
		#ip校验，防止内网IP误传入
    @staticmethod
    def is_intranet(ip):
        ret = ip.split('.')
        if not len(ret) == 4:
            return True
        if ret[0] == '10':
            return True
        if ret[0] == '172' and 16 <= int(ret[1]) <= 32:
            return True
        if ret[0] == '192' and ret[1] == '168':
            return True
        return False

    def _scan(self):
        thread_id = int( threading.currentThread().getName() )
        self.resolvers[thread_id].nameservers.insert(0, self.dns_servers[thread_id % self.dns_count])
        self.resolvers[thread_id].lifetime = self.resolvers[thread_id].timeout = 10.0      #超时时间10秒
        while self.queue.qsize() > 0 and not self.STOP_ME and self.found_count < 40000:    # 限制最大记录为 40000条
            sub = self.queue.get(timeout=1.0)
            for _ in range(3):
                try:
                    #拼接域名
                    cur_sub_domain = sub + '.' + self.target
                    #存入爆破成功的域名
                    answers = d.resolvers[thread_id].query(cur_sub_domain)
                    is_wildcard_record = False
                    if answers:
                        for answer in answers:
                            self.lock.acquire()
                            if answer.address not in self.ip_dict:
                                self.ip_dict[answer.address] = 1
                            else:
                                self.ip_dict[answer.address] += 1
                                if self.ip_dict[answer.address] > 2:    # a wildcard DNS record
                                    is_wildcard_record = True
                            self.lock.release()
                        if is_wildcard_record:
                            self._update_scan_count()
                            self._print_progress()
                            continue
                        ips = ', '.join([answer.address for answer in answers])
                        if (not self.ignore_intranet) or (not DnsQuery.is_intranet(answers[0].address)):
                            self.lock.acquire()
                            self.found_count += 1
                            msg = cur_sub_domain.ljust(30) + ips
                            sys.stdout.flush()
                            self.outfile.write(cur_sub_domain.ljust(30) + '\t' + ips + '\n')
                            self.lock.release()
                            try:
                                d.resolvers[thread_id].query('*.' + cur_sub_domain)
                            except:
                                for i in self.next_subs:
                                    self.queue.put(i + '.' + sub)
                        break
                except dns.resolver.NoNameservers, e:
                    break
                except Exception, e:
                    pass
            self._update_scan_count()
            self._print_progress()
        self._print_progress()
        self.lock.acquire()
        self.thread_count -= 1
        self.lock.release()

    def run(self):
        self.start_time = time.time()
        for i in range(self.threads_num):
            t = threading.Thread(target=self._scan, name=str(i))
            t.setDaemon(True)
            t.start()
        while self.thread_count > 1:
            try:
                time.sleep(1.0)
            except KeyboardInterrupt,e:
                msg = '[WARNING] User aborted, wait all slave threads to exit...'
                sys.stdout.flush()
                self.STOP_ME = True

if __name__ == '__main__':
    #传入域名
    parser = optparse.OptionParser('usage: %prog [options] target.com')
    #指定线程数
    parser.add_option('-t', '--threads', dest='threads_num',
              default=60, type='int',
              help='Number of threads. default = 60')
    #通过命令行传入文件，默认传入字典subnames.txt
    parser.add_option('-f', '--file', dest='names_file', default=False,
              type='string', help='Dict file used to brute sub names')
    #输出文件名为
    parser.add_option('-o', '--output', dest='output', default=None,
              type='string', help='Output file name. default is {target}.txt')

    (options, args) = parser.parse_args()
    if len(args) < 1:
        parser.print_help()
        sys.exit(0)

    d = DnsQuery(target=args[0], names_file=options.names_file,
                 ignore_intranet=options.i,
                 threads_num=options.threads_num,
                 output=options.output)
    d.run()
    while threading.activeCount() > 1:
	time.sleep(0.1)