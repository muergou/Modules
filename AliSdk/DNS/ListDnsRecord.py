#!/usr/bin/env python
#coding=utf-8


from aliyunsdkcore import client
from aliyunsdkalidns.request.v20150109 import DescribeDomainRecordsRequest
import sys
sys.path.append('..')
from Config import  accesskey
import json
from AliSdk.DNS import DescribeDomains


def ListDnsRecordPer(domain):
    clt = client.AcsClient(accesskey['accesskeyid'],accesskey['accesskeysecret'],'cn-hangzhou')
    listRequest = DescribeDomainRecordsRequest.DescribeDomainRecordsRequest()
    listRequest.set_DomainName(domain)
    listRequest.set_accept_format('json')
    listRequest.set_PageSize(100)
    listResult = json.loads(clt.do_action_with_exception(listRequest))
    return listResult

def ListDnsRecord():
    domains = DescribeDomains.DescribeDomains()
    print(domains)
    for i in xrange(len(domains)):
        dnsrecord = ListDnsRecordPer(domains[i])
        print dnsrecord


if __name__ == '__main__':
    ListDnsRecord()