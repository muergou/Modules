#!/usr/bin/python
# -*- coding: UTF-8 -*-


import psutil
import time
import MySQLdb
import urllib2,re

def get_public_ip():
    url = urllib2.urlopen("http://txt.go.sohu.com/ip/soip")
    text = url.read()
    ip = re.findall(r'\d+.\d+.\d+.\d+', text)
    return ip[0]

def format(f, n):
    if round(f)==f:
        m = len(str(f))-1-n
        if f/(10**m) ==0.0:
            return f
        else:
            return float(int(f)/(10**m)*(10**m))
    return round(f, n - len(str(int(f)))) if len(str(f))>n+1 else f

def db_operate(sql,sign) :
    if sign == 'check':
        db = MySQLdb.connect(host="192.168.220.148", port=3306, user="pydev", passwd="Pythondev123+-", db="opss",charset='utf8')
    else:
        db = MySQLdb.connect(host='192.168.220.148', port=3306, user="pydev", passwd="Pythondev123+-", db="opss",charset='utf8')
    cursor = db.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    db.commit()
    db.close()
    return data

def check_ram():
    ram = psutil.virtual_memory()
    ram_ava = format(ram.available/1073741824.0,3)
    ram_used = format(ram.used/1073741824.0,3)
    ram = [ram_used,ram_ava,ram.percent]
    return  ram

def check_cpu():
    cpu = psutil.cpu_times()
    cpu_total = cpu.user+cpu.idle
    cpu = format(cpu.user / cpu_total,3)
    return cpu

def check_disk():
    disk = psutil.disk_usage('/')
    disk_used = format(disk.used /1073741824.0,3 )
    disk_free = format(disk.free/1073741824.0,3)
    disk = [disk_used,disk_free,disk.percent]
    return disk

def time_record():
    start_time = time.strftime('%y-%m-%d', time.localtime(psutil.boot_time()))
    time_record = time.time()
    time_record = [start_time,time_record]
    return time_record

def compose_sql():
    ram = check_ram()
    disk = check_disk()
    cpu = check_cpu()
    time_red = time_record()
    mysql = check_mysql()
    tcp = check_tcp()
    public_ip = get_public_ip()
    sql = '''INSERT INTO hosts_status \
(public_ip,mysql_process, mysql_qps,tcp_listen,tcp_established,tcp_time_wait ,tcp_close_wait ,tcp_last_ack,tcp_sys_sent ,cpu_usage,ram_use,ram_free,ram_usage,time_stamp,disk_usage,disk_free,disk_used) \
VALUES ('%s',%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ;''' %\
          (public_ip,mysql[0],mysql[1],tcp['LISTEN'],tcp['ESTABLISHED'],tcp['TIME_WAIT'],tcp['CLOSE_WAIT'],tcp['LAST_ACK'],tcp['SYN_SENT'],cpu,ram[0],ram[1],ram[2],time_red[1],disk[0],disk[1],disk[2])
    return sql

def check_tcp():
    status_list = ["LISTEN", "ESTABLISHED", "TIME_WAIT", "CLOSE_WAIT", "LAST_ACK", "SYN_SENT"]
    status_temp = []
    tcp = {}
    net_connections = psutil.net_connections()
    #print(net_connections)
    for key in net_connections:
        status_temp.append(key.status)
    for status in status_list:
        tcp['%s' % status] = status_temp.count(status)
    return tcp

def check_mysql():
    #sql = '''SHOW FULL PROCESSLIST'''
    sql = '''show full processlist;'''
    data = db_operate(sql,'check')
    process=  len(data)
    sql = '''show global status like 'questions';'''
    qps = db_operate(sql,'check')
    mysql = []
    mysql.append(process)
    mysql.append(qps[0][1])
    #print process,qps[0][1]
    return mysql

if __name__ == "__main__" :
    operate = 'insert'
    sql = compose_sql()
    db_operate(sql,operate)

