#!/usr/bin/env python
#coding=utf-8

from aliyunsdkcore import client
from aliyunsdkcdn.request.v20141111 import DescribeDomainHitRateDataRequest
import datetime
from Config import accesskey


def DescribeDomainHitRateData(domain):
    StartDate = datetime.date.today() - datetime.timedelta(days=2)
    StopDate = datetime.date.today() - datetime.timedelta(days=1)
    clt = client.AcsClient(accesskey['accesskeyid'],accesskey['accesskeysecret'],'cn-hangzhou')
    request = DescribeDomainHitRateDataRequest.DescribeDomainHitRateDataRequest()
    request.set_accept_format('json')
    request.add_query_param('DomainName', domain)
    request.add_query_param('StartTime', '%sT16:00Z' % StartDate)
    request.add_query_param('EndTime', '%sT16:00Z' % StopDate)
    response = clt.do_action_with_exception(request)
    return response



if __name__ == '__main__':

    domain = 'www.t5b.net'
    DescribeDomainHitRateData(domain)









