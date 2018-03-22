#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-


import psutil
import prettytable
import time

startTime = time.time()

port = 80  # ssh -i /etc/ssh/ssh_host_rsa_key root@10.6.28.28

# define data structure for each connection, each ip is unique unit
ipaddress = {
    'ipaddress': None,
    'counts': 0,
    'stat': {
        'established': 0,
        'time_wait': 0,
        'others': 0
    }
}

# define data structure for statistics
statistics = {
    'portIsUsed': False,
    'portUsedCounts': 0,
    'portPeerList': [
        {
            'ipaddress': None,
            'counts': 0,
            'stat': {
                'established': 0,
                'time_wait': 0,
                'others': 0
            },
        },
    ]
}

tmp_portPeerList = list()
portPeerSet = set()
netstat = psutil.net_connections()

# get all ip address only for statistics data
for i, sconn in enumerate(netstat):

    if port in sconn.laddr:
        statistics['portIsUsed'] = True
        if len(sconn.raddr) != 0:
            statistics['portUsedCounts'] += 1
            ipaddress['ipaddress'] = sconn.raddr[0]
            tmp_portPeerList.append(str(ipaddress))  # dict() list() set() is unhashable type, collections.Counter

for ip in tmp_portPeerList:
    portPeerSet.add(str(ip))  # remove duplicated ip address using set()

for member in portPeerSet:
    statistics['portPeerList'].append(eval(member))

# add statistics data for each ip address
for sconn in netstat:
    if port in sconn.laddr:
        if len(sconn.raddr) != 0:
            for i, item in enumerate(statistics['portPeerList']):
                if item['ipaddress'] == sconn.raddr[0]:
                    statistics['portPeerList'][i]['counts'] += 1
                    if sconn.status == 'ESTABLISHED':
                        statistics['portPeerList'][i]['stat']['established'] += 1
                    elif sconn.status == 'TIME_WAIT':
                        statistics['portPeerList'][i]['stat']['time_wait'] += 1
                    else:
                        statistics['portPeerList'][i]['stat']['others'] += 1

# print statistics result using prettytable
if statistics['portIsUsed']:
    print "Total connections of port %s is %d." % (port, statistics['portUsedCounts'])
    table = prettytable.PrettyTable()
    table.field_names = ["Total Counts", "Remote IP Address", "Established Conns", "Time_wait Conns",
                         "Others Conns"]
    for i, ip in enumerate(statistics['portPeerList']):
        if ip['ipaddress'] is not None:
            table.add_row([ip['counts'], ip['ipaddress'], ip['stat']['established'], ip['stat']['time_wait'],
                           ip['stat']['others']])
    print table.get_string(sortby=table.field_names[1], reversesort=True)
else:
    print 'port %s has no connections, please make sure port is listen or in use.' % port

endTime = time.time()
print "Elapsed time: %s seconds." % (endTime - startTime)