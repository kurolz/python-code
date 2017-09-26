#!python2
#coding=utf-8

'''
IPy模块可以很好的辅助我们高效完成IP的规划工作。

此例根据输入的IP或子网返回网络、掩码、广播、反向解析、子网数、IP类型等信息
'''

from IPy import IP
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
ip_test = raw_input('请输入IP地址或网段地址：')
ips = IP(ip_test)
if len(ips) > 1:
 print ('网络地址：%s' % ips.net())
 print ('掩码：%s' % ips.netmask())
 print ('网络广播地址：%s' % ips.broadcast())
 print ('地址反向解析：%s' % ips.reverseNames())
 print ('网络子网数：%s' % len(ips))
else:
 print ('IP反向解析 %s' % ips.reverseNames())
print ('此IP地址转换成十六进制： %s' % ips.strHex())
print ('此IP地址转换成二进制： %s' % ips.strBin())
print ('此IP地址类型： %s' % ips.iptype())﻿