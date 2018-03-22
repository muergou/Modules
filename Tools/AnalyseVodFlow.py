#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append('..')
from AliSdk.CDN import GetAliCdnStatistics
from CloudflareSdk import GetCloudflareStatistics
import datetime
from Tools import DbOperate


def ComposeSql(chinadomain,foriegndomain):
    date = datetime.date.today() - datetime.timedelta(days=1)
    FlowData = GetAliCdnStatistics.GetFlowData(chinadomain)
    SrcFlowData = GetAliCdnStatistics.GetFlowSrcData(chinadomain)
    HitRate = GetAliCdnStatistics.GetHitRateData(chinadomain)
    ErrorHitRate = GetAliCdnStatistics.GetAveErrorRate(chinadomain)
    Cloudflare = GetCloudflareStatistics.AnalyseCloudflareData(foriegndomain)
    sql = '''INSERT INTO bandwidth_vod (date,flow_all_china,flow_back_china,hit_rate_china,error_rate_china,flow_all_foreign,flow_back_foreign,hit_rate_foreign,error_rate_foreign)\
VALUES\
("%s","%s","%s","%s","%s","%s","%s","%s","%s");''' % (date,str(FlowData)+'GB',str(SrcFlowData)+'GB',str(HitRate)+'%',str(ErrorHitRate)+'%',str(Cloudflare['FlowData'])+'GB',str(Cloudflare['FlowSrcData'])+'GB',str(Cloudflare['HitRate'])+'%',str(Cloudflare['ErrorHitRate'])+'%')

    return sql

def CommitDbOperate(chinadomain,foriegndomain):

    sql = ComposeSql(chinadomain,foriegndomain)
    DbOperate.DbOperate(sql)


if __name__ == '__main__':
    foriegndomain = 'vod79.com'
    chinadomain = 'www.t5b.net'
    CommitDbOperate(chinadomain,foriegndomain)