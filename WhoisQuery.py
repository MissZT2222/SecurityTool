#!/usr/bin/python
# -*- coding: utf-8 -*-

import whois
import json
import threadpool

def domain(dm):  #获取域名信息
    pfile = open("info%s.txt"%dm, "a+")
    info=whois.whois("%s"%dm)
    dminfo=json.loads(str(info))

#    print ("域名：",dminfo["domain_name"])
#    print("\n")
    if (isinstance(dminfo["domain_name"], list)):
        print (("域名："), str(dminfo["domain_name"][0]))
        pfile.write(str(dminfo["domain_name"][0]))
        pfile.write('\n')
    else:
        print ("域名：", str(dminfo["domain_name"]))
        pfile.write(str(dminfo["domain_name"]))
        pfile.write('\n')
    print ("国家：",str(dminfo["country"]))
    pfile.write(str(dminfo["country"]))
    pfile.write('\n')
    print ("公司：",str(dminfo["org"]))
    pfile.write(str(dminfo["org"]))
    pfile.write('\n')
    print ("地址：",str(dminfo["address"]))
    pfile.write(str(dminfo["address"]))
    pfile.write('\n')
    
    if (isinstance(dminfo["creation_date"], list)):
        print ("公司创建时间：", str(dminfo["creation_date"][0]))
        pfile.write(str(dminfo["creation_date"][0]))
        pfile.write('\n')
    else:
        print ("公司创建时间：", str(dminfo["creation_date"]))
        pfile.write(str(dminfo["creation_date"]))
        pfile.write('\n')

    if (isinstance(dminfo["emails"], list)):
        for email in dminfo["emails"]:
            print ("电子邮箱：", email)
            pfile.write(email)
            pfile.write('\n')
    else:
        print ("电子邮箱：", str(dminfo["emails"]))
        pfile.write(str(dminfo["emails"]))
        pfile.write('\n')

    if (isinstance(dminfo["updated_date"], list)):
        print ("最新更新时间：", str(dminfo["updated_date"][0]))
    else:
        print ("最新更新时间：", str(dminfo["updated_date"]))
            
    if (isinstance(dminfo["expiration_date"], list)):
        print ("到期时间：", str(dminfo["expiration_date"][0]))
        pfile.write(str(dminfo["expiration_date"][0]))
        pfile.write('\n')
    else:
        print ("到期时间：", str(dminfo["expiration_date"]))
        pfile.write(str(dminfo["expiration_date"]))
        pfile.write('\n')
    print ("whois服务器：",str(dminfo["whois_server"]))
    pfile.write(str(dminfo["whois_server"]))
    pfile.write('\n')

    if(isinstance(dminfo["name_servers"],list)):
        for dnsserver in dminfo["name_servers"]:
            print ("dns 服务器：",dnsserver)
            pfile.write(dnsserver)
            pfile.write('\n')
    else:
        print (("dns服务器："),str(dminfo["name_servers"]))

if __name__ == "__main__":

    dmfile = open('data.txt', 'r')
    dm = []
    with open('data.txt', 'r') as f:
        print(f.read())
    for line in dmfile.readlines():
        dm.append(line.strip('\n'))#去除换行符
    dmfile.close()

    pool = threadpool.ThreadPool(20)
    requests = threadpool.makeRequests(domain, dm)
    [pool.putRequest(req) for req in requests]
    pool.wait()