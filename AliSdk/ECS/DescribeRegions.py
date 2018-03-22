#!/usr/bin/env python
#coding=utf-8


from aliyunsdkcore import client
from aliyunsdkecs.request.v20140526 import DescribeRegionsRequest
from Config import accesskey
import json


def DescribeRegions():
    clt = client.AcsClient(accesskey['accesskeyid'],accesskey['accesskeysecret'])
    request = DescribeRegionsRequest.DescribeRegionsRequest()
    request.set_accept_format('json')
    response = clt.do_action_with_exception(request)
    response = json.loads(response)
    return response['Regions']['Region']


if __name__ == '__main__':
    DescribeRegions()