#!/usr/bin/env python
#coding=utf-8


from aliyunsdkcore import client
from aliyunsdkalidns.request.v20150109 import DescribeDomainsRequest
import sys,json
sys.path.append('..')
from Config import  accesskey



def DescribeDomains():
    clt = client.AcsClient(accesskey['accesskeyid'],accesskey['accesskeysecret'],'cn-hangzhou')
    request = DescribeDomainsRequest.DescribeDomainsRequest()
    request.set_accept_format('json')
    response = clt.do_action_with_exception(request)
    response = json.loads(response)
    print response['Domains']['Domain']
    domains = []
    for i in xrange(len(response['Domains']['Domain'])):
        #domains.append(response['Domains']['Domain'][i]['DomainName'])
        print response['Domains']['Domain'][i]


if __name__ == '__main__':
    DescribeDomains()