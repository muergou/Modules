#!/usr/bin/env python  
# -*- coding: utf-8 -*-

import urllib2  
import socket


#检查网站返回码
def GetWebCode(url,headers):
    req = urllib2.Request(url=url,headers=headers)
    data = urllib2.urlopen(req).getcode()
    return data 

#检查端口状态
def CheckPortStatus(ip,port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex((ip,port))
    if result == 0:
       return "open"
    else:
       return "down"

#查看网站返回数据
def GetWebContent(url,headers):
    req = urllib2.Request(url=url,headers=headers)
    data = urllib2.urlopen(req).read()
    return data
