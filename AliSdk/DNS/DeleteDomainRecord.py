#!/usr/bin/env python
#coding=utf-8

from aliyunsdkcore import client
from aliyunsdkalidns.request.v20150109 import DeleteDomainRecordRequest
import sys
sys.path.append('..')
from Config import  accesskey


def DeleteDomainRecord(sldomain):
    clt = client.AcsClient(accesskey['accesskeyid'],accesskey['accesskeysecret'],'cn-hangzhou')
    delRequest = DeleteDomainRecordRequest.DeleteDomainRecordRequest()
    delRequest.set_RecordId(sldomain)
    delResult = clt.do_action_with_exception(delRequest)
    return delResult
    