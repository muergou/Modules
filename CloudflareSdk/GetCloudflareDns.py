#!/usr/bin/env python
# -*- coding: utf-8 -*-


from Config import apikey_cloudflare,zone_ids
from Tools.GetWebStatus import GetWebContent
import sys
import json
from Tools import DbOperate
sys.path.append('..')



def GetDnsRecord():
    domain = zone_ids.keys()
    headers = {"X-Auth-Email":"41664321@qq.com","X-Auth-Key":"%s" % apikey_cloudflare ,"Content-Type":" application/json"}
    for i in range(len(zone_ids)):
        url = "https://api.cloudflare.com/client/v4/zones/%s/dns_records" % zone_ids['%s' % domain[i]]
        dns_record = GetWebContent(url,headers)
        dns_record = json.loads(dns_record)
        for j in range(len(dns_record['result'])):
            try:
                name =  dns_record['result'][j]['name']
            except:
                name = "none"
            try:
                proxy = dns_record['result'][j]['proxied']
                if str(proxy).lower() == 'true':
                    proxy = 'cloudflare'
            except:
                proxy = "none"
            try:
                content = dns_record['result'][j]['content']
            except:
                content = "none"
            try:
                types = dns_record['result'][j]['type']
            except:
                types = "none"


            sql = '''INSERT INTO second_level_domain(second_level_domain,ip_address,type,cdn_factory,dns_factory)\
VALUES ("%s","%s","%s","%s","cloudflare");'''%(name,content,types,proxy)
            DbOperate.DbOperate(sql)
            print sql


if __name__ == '__main__':
    GetDnsRecord()