#!/usr/bin/env python
#coding=utf-8

import sys
sys.path.append('..')
from Tools import DbOperate
import time
import SendGMail





def ComposrSql():
    sql = "SELECT inuse,cloud_factory, public_ip,position,end_time FROM cloud_hosts WHERE warn=1"
    data = DbOperate.DbOperate(sql)
    return data

def CheckMaturity():
    toaddr='1586086424@qq.com'
    cloudhosts = ComposrSql()
    localtime = time.time()
    for i in xrange(len(cloudhosts)):
        endtime = cloudhosts[i][4]
        endtime = int(time.mktime(time.strptime(endtime,"%Y-%m-%dT%H:%M:%SZ")))
        if endtime-localtime >=0 and endtime-localtime <= 2592000:
            mailifo = '%s host %s is almost maturity,position: %s,check please' %(cloudhosts[i][1],cloudhosts[i][0],cloudhosts[i][3])
            print(mailifo)
            '''try:
                result=SendGMail.SendMail(mailifo,toaddr)
                if result == 0:
                    continue
            except:
                print "error in sendmail"
                continue'''

if __name__ == '__main__':
    data = ComposrSql()
    print(data)
    CheckMaturity()