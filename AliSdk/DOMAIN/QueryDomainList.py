#!/usr/bin/env python
#coding=utf-8

import sys, json
sys.path.append('..')
from Config import accesskey
from aliyunsdkcore import client
from aliyunsdkdomain.request.v20180129 import QueryDomainListRequest
from Tools import DbOperate


def QueryDomainList():
    clt = client.AcsClient(accesskey['accesskeyid'], accesskey['accesskeysecret'], 'cn-hangzhou')
    request = QueryDomainListRequest.QueryDomainListRequest()
    request.set_accept_format('json')
    request.set_PageSize('100')
    request.set_PageNum('1')
    response = json.loads(clt.do_action_with_exception(request))
    return response


def QueryDomainInstanceIdList():

    domainlist = QueryDomainList()
    domaininstanceidlist = []
    for i in xrange(len(domainlist['Data']['Domain'])):
        domaininstanceidlist.append(domainlist['Data']['Domain'][i]['InstanceId'])
        #print domainlist['Data']['Domain'][i]['InstanceId']
        #print domainlist['Data']['Domain'][i]['DomainName'],domainlist['Data']['Domain'][i]['ExpirationDate'],domainlist['Data']['Domain'][i]['RegistrationDate']
    return domaininstanceidlist

if __name__ == '__main__':
    QueryDomainInstanceIdList()