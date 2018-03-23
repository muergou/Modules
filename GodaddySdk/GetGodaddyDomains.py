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
    domainslist = GetDomains()
    domainsinfo = []
    for i in range(len(domainslist)):
        domaininfo = {}
        ssokey = "sso-key " + apikey['key'] +":"+ apikey['secret']
        url = "https://api.godaddy.com/v1/domains/%s" % domainslist[i]
        headers = {'User-Agent' :'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',"Authorization": "%s" % ssokey }
        data = GetWebContent(url,headers)
        domaindetail = json.loads(data)
        if domaindetail['status'] == 'CANCELLED':
            continue
        else:
            domainname = domaindetail['domain']
            createdtime = domaindetail['createdAt']
            endtime = domaindetail['expires']
            try:
                deadtime = domaindetail['renewDeadline']
            except:
                deadtime = "none"
            try:
                if "CLOUDFLARE" in domaindetail['nameServers'][0].upper():
                    nameserver = "cloudflare"
                elif "ffdns" in domaindetail['nameServers'][0].lower():
                    nameserver = "cloudxns"
                elif "maff" or "alidns" in domaindetail['nameServers'][0].lower():
                    nameserver = "aliyun"
                elif "xz.com" in domaindetail['nameServers'][0].lower():
                    nameserver = "xz"
                else :
                    nameserver = domaindetail['nameServers'][0]
            except:
                nameserver = "none"
        domaininfo.setdefault("domain",domainname)
        domaininfo.setdefault("create",createdtime)
        domaininfo.setdefault("end",endtime)
        domaininfo.setdefault("dead",deadtime)
        domaininfo.setdefault("dns",nameserver)
        domainsinfo.append(domaininfo)

    #print domainsinfo
    return domainsinfo

def InsertSql():
    domainsinfo = GetDomainDetails()
    for i in xrange(len(domainsinfo)):
        sql = '''INSERT INTO domain_name (domain,domain_factory,start_time,end_time, dns_factory,dead_time,warn)\
    VALUES \
    ("%s","Godaddy","%s","%s","%s","%s",1); '''%(domainsinfo[i]['domain'],domainsinfo[i]['create'],domainsinfo[i]['end'],domainsinfo[i]['dns'],domainsinfo[i]['dead'])

        #print sql
        DbOperate.DbOperate(sql)

if __name__ == '__main__':
    InsertSql()
