#!python3
# coding: utf-8
#

'''连接mysql数据库并执行SQL语句'''

import os,sys
import pymysql
try:
    conn = pymysql.connect(host='localhost',user='root',passwd='',db='db_student')
except Exception as e:
    print (e)
    sys.exit()
cursor = conn.cursor()
sql = "select * from stu_inf"
cursor.execute(sql)
data = cursor.fetchall()
if data:
    for x in data:
    print (x[0],x[1],x[2],x[3],x[4],x[5])
cursor.close()
conn.close()﻿​