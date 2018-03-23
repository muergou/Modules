#!/usr/bin/env python
#-*- coding:utf-8 -*-


from cloudxns.api import *
import json
import sys
sys.path.append('..')
from Config import cloudxns
from Tools import DbOperate


api = Api(api_key=cloudxns['apikey'], secret_key=cloudxns["secretkey"])
def GetActiveDomain():
    domaindetail = json.loads(api.domain_list())

    domainlist = []
    for i in xrange(len(domaindetail['data'])):
        domainid = {}
        if domaindetail['data'][i]['take_over_status'] == 'Taken over':
            domainid.setdefault("domain",domaindetail['data'][i]['domain'])
            domainid.setdefault("id",domaindetail['data'][i]['id'])
            domainlist.append(domainid)
    #print domainlist
    return domainlist


def GetDomainRecord():
    domainlist = GetActiveDomain()
    for i in xrange(len(domainlist)):
        #print domainlist[i]['domain']
        domainid =  domainlist[i]['id']
        domainrecord = json.loads(api.record_list(domainid,row_num=100))

        #print(domainrecord)
        if domainrecord['message'] == 'success' :
            for j in xrange(len(domainrecord['data'])):
                if str(domainrecord['data'][j]['type']) != 'TXT':
                    try:
                        value =  domainrecord['data'][j]['value']
                    except:
                        value = 'error'
                    try:
                        domain = str(domainrecord['data'][j]['host']) + '.' + domainlist[i]['domain']
                    except:
                        domain = 'error'
                    try:
                        type = domainrecord['data'][j]['type']
                    except:
                        value = 'error'
                    sql =  '''INSERT INTO second_level_domain(second_level_domain,ip_address,type,cdn_factory,dns_factory)\
    VALUES ("%s","%s","%s","nodata","cloudxns");''' % (domain,value,type,)
                    #print  sql
                    DbOperate.DbOperate(sql)
                else:
                    continue
        else:
            continue
if __name__ == '__main__':
    GetDomainRecord()