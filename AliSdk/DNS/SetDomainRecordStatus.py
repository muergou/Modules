#!/usr/bin/env python
#coding=utf-8

from aliyunsdkcore import client
import sys
from aliyunsdkalidns.request.v20150109 import SetDomainRecordStatusRequest
sys.path.append('..')
import json
from Config import  accesskey



def SetDomainRecordStatus(sldomain,status):
    clt = client.AcsClient(accesskey['accesskeyid'],accesskey['accesskeysecret'],'cn-hangzhou')
    setRequest = SetDomainRecordStatusRequest.SetDomainRecordStatusRequest()
    setRequest.set_RecordId(sldomain)
    setRequest.set_Status(status)
    setResult = clt.do_action_with_exception(setRequest)
    return setResult