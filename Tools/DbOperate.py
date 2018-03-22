#!/usr/bin/python
# -*- coding: UTF-8 -*-

import MySQLdb
import sys
sys.path.append('..')
from Config import mysql


def DbOperate(sql) :
    host = mysql['host']
    port = mysql['port']
    user = mysql['username']
    passwd = mysql['password']
    database = mysql['database']
    charset = mysql['charset']
    db = MySQLdb.connect(host=host, port=port, user=user, passwd=passwd, db=database,charset=charset)
    cursor = db.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    db.commit()
    db.close()
    return data

if __name__ == '__main__':
    sql = "select * from bandwidth_vod"
    data = DbOperate(sql)
    print(data)

