#!/usr/bin/env python
# -*- coding: utf-8 -*-

from aliyunsdkcore import client
from aliyunsdkecs.request.v20140526 import DescribeInstancesRequest
import DescribeRegions
from AliSdk.config import accesskey
import json



def DescribeInstancesPerzone(zoneid):
    clt = client.AcsClient(accesskey['accesskeyid'],accesskey['accesskeysecret'])
    request = DescribeInstancesRequest.DescribeInstancesRequest()
    request.set_accept_format('json')
    request.add_query_param('RegionId', zoneid)
    response = clt.do_action_with_exception(request)
    return response



def DescribeInstances():
    zones = DescribeRegions.DescribeRegions()
    for i in xrange(len(zones)):
        instances = json.loads(DescribeInstancesPerzone(zones[i]['RegionId']))
        #print(instances)
        if instances['TotalCount'] != 0:
            for i in range(instances['TotalCount']):
                sql = "UPDATE `cloud_hosts` SET "
                try:
                    mac = instances['Instances']['Instance'][i]['NetworkInterfaces']['NetworkInterface'][0]['MacAddress']
                except:
                    mac = "none"
                try:
                    pri_ip = instances['Instances']['Instance'][i]['NetworkInterfaces']['NetworkInterface'][0][
                        'PrimaryIpAddress']
                except:
                    pri_ip = "none"
                band_width = instances['Instances']['Instance'][i]['InternetMaxBandwidthIn']
                charge_type = instances['Instances']['Instance'][i]['InternetChargeType']
                ram = instances['Instances']['Instance'][i]['Memory']
                cpu = instances['Instances']['Instance'][i]['Cpu']
                start_time = instances['Instances']['Instance'][i]['StartTime']
                ins_name = instances['Instances']['Instance'][i]['InstanceName']
                os_name = instances['Instances']['Instance'][i]['OSName']
                try:
                    pub_ip = instances['Instances']['Instance'][i]['PublicIpAddress']['IpAddress'][0]
                except:
                    pub_ip = "none"
                host_name = instances['Instances']['Instance'][i]['HostName']
                position = instances['Instances']['Instance'][i]['RegionId']
                end_time = instances['Instances']['Instance'][i]['ExpiredTime']
                username = "default"
                password = "default"
                disk = "default"
                sql1 = "host_name='%s',primary_ip='%s',public_ip='%s',mac ='%s',ram='%s',cpu_num='%s',disk='%s',os='%s',end_time='%s',billing_methods='%s',bandwidth='%s' WHERE inuse='%s'" % \
                       (host_name, pri_ip, pub_ip, mac, ram, cpu, disk, os_name, end_time, charge_type, band_width,
                        ins_name)
                # sql1 = '(%d,"%s","aliyun","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")' % \
                #    (id,ins_name,host_name,pri_ip,pub_ip,mac,cpu,ram,disk,os_name,username,password,start_time,end_time,position,charge_type,band_width)
                # id = id + 1
                # if i+1 < data['TotalCount']:
                #    sql = sql + sql1 + ","
                # else:
                #    sql = sql + sql1 + ";"
                sql = sql + sql1 + ";"
                print(sql)


if __name__ == '__main__':
    zoneid = 'cn-qingdao'
    DescribeInstances()