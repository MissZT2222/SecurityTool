#爆破目录程序
import queue
import urllib3
import threading
import sys
import time

#3.定义路径获取函数get_path()
def get_path(url,file = "mulu.txt"):
    path_queue = queue.Queue()
    f = open(file, "r", encoding="utf-8")
    for i in f.readlines():
        path = url + i.strip()
        path_queue.put(path)
    f.close()
    return path_queue

#5.定义目录爆破函数get_url()
def get_url(path_queue):
    while not path_queue.empty():
        try:
			#取消控制台关于访问http网站的告警
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            url = path_queue.get()
            http = urllib3.PoolManager()
            respone = http.request('GET', url)
            if respone.status == 200:
                print("[%d] => %s" % (respone.status, url))

        except:
            pass
    else:
        sys.exit()

def main(url, threadNum):
    #2.以队列的方式获取要爆破的路径
    path_queue = get_path(url)

    # 4.利用多线程进行url目录爆破
    threads = []
    for i in range(threadNum):
        t = threading.Thread(target=get_url, args=(path_queue, ))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

if __name__ == "__main__":
    #1.输入Url和线程大小
    start = time.time()
    url = "www.xazlsec.com"
    threadnum = 200
    main(url, threadnum)
    end = time.time()
    print("总共耗时 %.2f" % (end-start))