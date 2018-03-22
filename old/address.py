#!/usr/bin/env python
# -*- coding: utf-8 -*-

import uuid
import socket
import urllib2
import re


def get_mac_address():
    node = uuid.getnode()
    mac = uuid.UUID(int=node).hex[-12:]
    return mac


def get_intranet_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


def get_host_name():
    host_name = socket.getfqdn(socket.gethostname())
    return host_name


def get_public_ip():
    url = urllib2.urlopen("http://txt.go.sohu.com/ip/soip")
    text = url.read()
    ip = re.findall(r'\d+.\d+.\d+.\d+', text)
    return ip[0]