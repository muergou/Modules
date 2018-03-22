#!/usr/bin/env python
# -*- coding: utf-8 -*-

from aliyunsdkcore import client
from Config import accesskey
from aliyunsdkcdn.request.v20141111 import RefreshObjectCachesRequest

def RefreshAliCache(domain):
    accesskeyid = accesskey['accesskeyid']
    accesskeysecret = accesskey['accesskeysecret']
    url = "http://" + domain + "/"
    Client = client.AcsClient(accesskeyid,accesskeysecret)
    request = RefreshObjectCachesRequest.RefreshObjectCachesRequest()
    request.set_accept_format('json')
    request.set_ObjectPath(url)
    request.set_ObjectType("Directory")
    result = Client.do_action_with_exception(request)
    return result
