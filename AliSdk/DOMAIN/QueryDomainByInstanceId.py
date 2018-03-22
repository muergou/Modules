#!/usr/bin/env python
#coding=utf-8

from aliyunsdkcore import client
from aliyunsdkdomain.request.v20180129 import QueryDomainByInstanceIdRequest
import QueryDomainList
import sys,json
sys.path.append('..')
from Config import  accesskey
from Tools import DbOperate

def QueryDomainByInstanceId(instanceid):
    clt = client.AcsClient(accesskey['accesskeyid'], accesskey['accesskeysecret'], 'cn-hangzhou')
    request = QueryDomainByInstanceIdRequest.QueryDomainByInstanceIdRequest()
    request.set_accept_format('json')
    request.set_InstanceId(instanceid)
    response = clt.do_action_with_exception(request)
    return response



def insertintosql():
    domaininstanceidlist = QueryDomainList.QueryDomainInstanceIdList()
    for i in xrange(len(domaininstanceidlist)):
        domaindetail = json.loads(QueryDomainByInstanceId(domaininstanceidlist[i]))
        #print domaindetail['ExpirationDate'],domaindetail['RegistrationDate'],domaindetail['DomainName'],domaindetail['DnsList']['Dns'][1]

        if "cloudflare" in domaindetail['DnsList']['Dns'][1].lower():
            nameserver = "cloudflare"
        elif "ffdns" in domaindetail['DnsList']['Dns'][1].lower():
            nameserver = "cloudxns"
        elif "maff" or "alidns" or 'hichina' in domaindetail['DnsList']['Dns'][1].lower():
            nameserver = "aliyun"
        elif "xz.com" in domaindetail['DnsList']['Dns'][1].lower():
            nameserver = "xz"
        else:
            nameserver = domaindetail['DnsList']['Dns'][1]

        sql = '''INSERT INTO domain_name (domain,domain_factory,start_time,end_time, dns_factory)\
VALUES \
("%s","aliyun","%s","%s","%s"); ''' % (domaindetail['DomainName'],domaindetail['RegistrationDate'],domaindetail['ExpirationDate'],nameserver)

        DbOperate.DbOperate(sql)

if __name__ == '__main__':
    insertintosql()
