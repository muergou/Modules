#!/usr/bin/env python
#-*- coding:utf-8 -*-


from cloudxns.api import *
import json
import sys
sys.path.append('..')
from Config import cloudxns


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
    return domainlist


def GetDomainRecord():
    domainlist = GetActiveDomain()
    for i in xrange(len(domainlist)):
        print domainlist[i]['domain']
        domainid =  domainlist[i]['id']
        domainrecord = json.loads(api.record_list(domainid))
        print(domainrecord)
        '''try:
            for j in xrange(len(domainrecord['data'])):
                print domainrecord['data'][i]['value'],domainrecord['data'][i]['host'],domainrecord['data'][i]['type']
        except:
            print("no data")'''



if __name__ == '__main__':
    GetDomainRecord()
