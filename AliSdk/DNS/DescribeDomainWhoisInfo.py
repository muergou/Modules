#!/usr/bin/env python
#coding=utf-8


from aliyunsdkcore import client
from aliyunsdkalidns.request.v20150109 import DescribeDomainWhoisInfoRequest
import sys,json
sys.path.append('..')
from Config import  accesskey


def DescribeDomainWhoisInfo(domain):
    clt = client.AcsClient(accesskey['accesskeyid'], accesskey['accesskeysecret'], 'cn-hangzhou')
    request = DescribeDomainWhoisInfoRequest.DescribeDomainWhoisInfoRequest()
    request.set_accept_format('json')
    request.set_DomainName(domain)
    response = json.loads(clt.do_action_with_exception(request))
    return response


def CheckDomainIfBelongAli(domain):
    clt = client.AcsClient(accesskey['accesskeyid'], accesskey['accesskeysecret'], 'cn-hangzhou')
    request = DescribeDomainWhoisInfoRequest.DescribeDomainWhoisInfoRequest()
    request.set_accept_format('json')
    request.set_DomainName(domain)
    response = json.loads(clt.do_action_with_exception(request))
    if 'hichina' or 'alidns' in str(response['DnsServers']['DnsServer'][0]).lower():
        return 1
    else:
        return 0


if __name__ == '__main__':
    domain = 't5b.net'
    id = CheckDomainIfBelongAli(domain)
    print(id)