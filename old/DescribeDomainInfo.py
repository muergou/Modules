#!/usr/bin/env python
#coding=utf-8

from aliyunsdkcore import client
import sys
sys.path.append('..')
from Config import accesskey
from aliyunsdkalidns.request.v20150109 import DescribeDomainInfoRequest
import old.DescribeDomains
import json


def DescribeDomainInfo(domain):
    clt = client.AcsClient(accesskey['accesskeyid'], accesskey['accesskeysecret'], 'cn-hangzhou')
    request = DescribeDomainInfoRequest.DescribeDomainInfoRequest()
    request.set_DomainName(domain)
    request.set_accept_format('json')
    response = clt.do_action_with_exception(request)
    response = json.loads(response)
    return response

def GetAllDomainInfo():
    domains = old.DescribeDomains.DescribeDomains()
    alldomaininfo = []
    for i in xrange(len(domains)):
        domainsinfo = DescribeDomainInfo(domains[i])
        domaininfo = {}
        domain = domainsinfo['DomainName']
        if 'hichina' in domainsinfo['DnsServers']['DnsServer'][1].lower():
            dnsserver = 'wanwang'
        elif 'alidns' in domainsinfo['DnsServers']['DnsServer'][1].lower():
            dnsserver = 'aliyun'
        else:
            dnsserver = 'none'
        domaininfo.setdefault("domain",domain)
        domaininfo.setdefault("dnsserver",dnsserver)
        alldomaininfo.append(domaininfo)
        print alldomaininfo


if __name__ == '__main__':
    GetAllDomainInfo()