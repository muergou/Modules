#!/usr/bin/env python
# -*- coding: utf-8 -*-

from AliSdk.CDN import DescribeDomainFlowData, DescribeDomainHitRateData, DescribeDomainHttpCodeData, \
    DescribeDomainSrcFlowData
import json
import sys
sys.path.append("..")
from Tools import NumFormat

#总流量
def GetFlowData(domain):
    FlowData = json.loads(DescribeDomainFlowData.DescribeDomainFlowData(domain))
    FlowDataNum = 0
    for i in  xrange(len(FlowData['FlowDataPerInterval']['DataModule'])):
        FlowDataNum = FlowDataNum + int(FlowData['FlowDataPerInterval']['DataModule'][i]['Value'])
    FlowDataNum = NumFormat.format(FlowDataNum/1073741824.0 ,3)

    return FlowDataNum
#回源流量
def GetFlowSrcData(domain):
    FlowSrcData = json.loads(DescribeDomainSrcFlowData.DescribeDomainSrcFlowData(domain))
    FlowSrcDataNum = 0
    for i in xrange(len(FlowSrcData['SrcFlowDataPerInterval']['DataModule'])):
        FlowSrcDataNum = FlowSrcDataNum + int(FlowSrcData['SrcFlowDataPerInterval']['DataModule'][i]['Value'])
    FlowSrcDataNum = NumFormat.format(FlowSrcDataNum /1073741824.0,3)
    return FlowSrcDataNum
#命中率
def GetHitRateData(domain):
    HitRateData = json.loads(DescribeDomainHitRateData.DescribeDomainHitRateData(domain))
    HitRateDataNum = 0
    for i in range(len(HitRateData['HitRateInterval']['DataModule'])):
        HitRateDataNum = HitRateDataNum + float(HitRateData['HitRateInterval']['DataModule'][i]['Value'])

    AveHitRateData = NumFormat.format(HitRateDataNum / len(HitRateData['HitRateInterval']['DataModule']),4)
    return AveHitRateData
#错误率
def GetAveErrorRate(domain):
    HttpCodeData = json.loads(DescribeDomainHttpCodeData.DescribeDomainHttpCodeData(domain))
    BadHttpCodeNum = 0
    HttpCodeNum = 0
    for i in range(len(HttpCodeData['HttpCodeData']['UsageData'])):
        for j in range(len(HttpCodeData['HttpCodeData']['UsageData'][i]['Value']['CodeProportionData'])):
            HttpCodeNum = HttpCodeNum + int(HttpCodeData['HttpCodeData']['UsageData'][i]['Value']['CodeProportionData'][j]['Count'])
            if int(HttpCodeData['HttpCodeData']['UsageData'][i]['Value']['CodeProportionData'][j]['Code']) >= 500:
                BadHttpCodeNum = BadHttpCodeNum + int(HttpCodeData['HttpCodeData']['UsageData'][i]['Value']['CodeProportionData'][j]['Count'])
    AveErrorRate = NumFormat.format(BadHttpCodeNum*100.0/HttpCodeNum,5)
    return AveErrorRate


if __name__ == '__main__':
    domain = 'www.t5b.net'
    data = GetFlowSrcData(domain)
    print(data)