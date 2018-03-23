#!/usr/bin/env python
# -*- coding: utf-8 -*-



import sys
sys.path.append('..')
import DbOperate
import time
import SendGMail


def ComposrSql():
    sql = "SELECT * FROM domain_name WHERE warn=1"
    data = DbOperate.DbOperate(sql)
    return data

def CheckMaturity():
    toaddr='1586086424@qq.com'
    domains = ComposrSql()
    localtime = time.time()
    for i in xrange(len(domains)):
        endtime = domains[i][4]
        endtime = int(time.mktime(time.strptime(endtime,"%Y-%m-%dT%H:%M:%SZ")))
        if endtime-localtime >=0 and endtime-localtime <= 2592000:
            mailifo = '%sdomain %s is almost maturity,check please' %(domains[i][3],domains[i][1])
            print(mailifo)
            try:
                result=SendGMail.SendMail(mailifo,toaddr)
                if result == 0:
                    continue
            except:
                print "error in sendmail"
                continue



if __name__ == '__main__':
    CheckMaturity()