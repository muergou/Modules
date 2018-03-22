#!/usr/bin/env python
# -*- coding: utf-8 -*-



from Config import apikey_cloudflare,zone_ids
from Tools.GetWebStatus import GetWebContent
import json
import datetime
import sys
sys.path.append('..')
from Tools import NumFormat


def GetCloudflareBandwidth(domain):
    StartDate = datetime.date.today() - datetime.timedelta(days=2)
    StopDate = datetime.date.today() - datetime.timedelta(days=1)
    Headers = {"X-Auth-Email":"41664321@qq.com","X-Auth-Key":"%s" % apikey_cloudflare ,"Content-Type":" application/json"}
    Url = "https://api.cloudflare.com/client/v4/zones/%s/analytics/dashboard?since=%sT16:00:00Z&until=%sT16:00:00Z&continuous=true" % (zone_ids[domain],StartDate,StopDate)
    Data = GetWebContent(Url,Headers)
    Data = json.loads(Data)
    return Data
def AnalyseCloudflareData(domain):
    Data = GetCloudflareBandwidth(domain)
    FlowData = NumFormat.format(int(Data['result']['totals']['bandwidth']['all']) /1073741824.0 ,3)
    FlowSrcData  = NumFormat.format(int(Data['result']['totals']['bandwidth']['uncached']) /1073741824.0,3)
    HitRate = NumFormat.format(FlowSrcData *100.0/FlowData ,3)
    HttpStatus = Data['result']['totals']['requests']['http_status']
    HttpStatusAll = Data['result']['totals']['requests']['all']
    BadHttpCodeNum = 0
    for i in xrange(len(HttpStatus.keys())):
        if int(HttpStatus.keys()[i]) >= 500:
            BadHttpCodeNum = BadHttpCodeNum + HttpStatus['%s' % HttpStatus.keys()[i]]
            #print(HttpStatus.keys()[i])
    AveErrorRate = NumFormat.format(BadHttpCodeNum*100.0/HttpStatusAll,5)
    CloudflareData = {"FlowData":"%s" % FlowData,"FlowSrcData":"%s" % FlowSrcData,"HitRate":"%s" % HitRate,"ErrorHitRate":"%s" % AveErrorRate}
    return CloudflareData

if __name__ == '__main__':
    AnalyseCloudflareData('kkp7.com')