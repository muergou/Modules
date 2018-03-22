#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Config import apikey
from Tools.GetWebStatus import GetWebContent
import  json
from Tools import DbOperate


def GetDomains():
    sso_key = "sso-key " + apikey['key'] +":"+ apikey['secret']
    url = "https://api.godaddy.com/v1/domains/"
    headers = {'User-Agent' :'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',"Authorization": "%s" % sso_key }
    data = GetWebContent(url,headers)
    domain_dict = json.loads(data)
    domains_list = []
    for i in range(len(domain_dict)):
        domain = domain_dict[i]['domain']
        try:
            domains_list.append(domain)
        except:
            print type(domains_list)
    return  domains_list

def GetDomainDetails():
    domains_list = GetDomains()
    domainsinfo = []
    for i in range(len(domains_list)):
        domaininfo = {}
        sso_key = "sso-key " + apikey['key'] +":"+ apikey['secret']
        url = "https://api.godaddy.com/v1/domains/%s" % domains_list[i]
        #print(url)
        headers = {'User-Agent' :'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',"Authorization": "%s" % sso_key }
        data = GetWebContent(url,headers)
        domain_detail = json.loads(data)
        if domain_detail['status'] == 'CANCELLED':
            continue
        else:
            domain_name = domain_detail['domain']
            created_time = domain_detail['createdAt']
            end_time = domain_detail['expires']
            try:
                dead_time = domain_detail['renewDeadline']
            except:
                dead_time = "none"
            try:
                if "CLOUDFLARE" in domain_detail['nameServers'][0].upper():
                    name_server = "cloudflare"
                elif "ffdns" in domain_detail['nameServers'][0].lower():
                    name_server = "cloudxns"
                elif "maff" or "alidns" in domain_detail['nameServers'][0].lower():
                    name_server = "aliyun"
                elif "xz.com" in domain_detail['nameServers'][0].lower():
                    name_server = "xz"
                else :
                    name_server = domain_detail['nameServers'][0]
            except:
                name_server = "none"
        domaininfo.setdefault("domain",domain_name)
        domaininfo.setdefault("create",created_time)
        domaininfo.setdefault("end",end_time)
        domaininfo.setdefault("dead",dead_time)
        domaininfo.setdefault("dns",name_server)
        domainsinfo.append(domaininfo)

    print domainsinfo
    return domainsinfo

def InsertSql():
    domainsinfo = GetDomainDetails()
    for i in xrange(len(domainsinfo)):
        sql = '''INSERT INTO domain_name (domain,domain_factory,start_time,end_time, dns_factory,dead_time)\
    VALUES \
    ("%s","Godaddy","%s","%s","%s","%s"); '''%(domainsinfo[i]['domain'],domainsinfo[i]['create'],domainsinfo[i]['end'],domainsinfo[i]['dns'],domainsinfo[i]['dead'])

        #print sql
        DbOperate.DbOperate(sql)

if __name__ == '__main__':
    InsertSql()
