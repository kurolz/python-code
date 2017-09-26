#!python3
#coding=utf-8

'''
大部分的DNS解析是一个域名对应一个IP地址，但是通过DNS轮循技术可将一个域名对应多个IP地址，这样可以实现简单且高效的负载平衡，但是轮循技术有一个缺点就是当目标主机不可用时，不能自动的删除，所以引出了要对业务主机的服务的可用性进行监控。

#本例通过分析当前域名的解析IP，再结合服务端口探测来实现自动监控，在域名解析中添加、删除IP时，无须对监控脚步更改。
'''


import dns.resolver
import os
import http.client

iplist=[]	#定义域名IP列表变量
appdomain="www.google.cn"	#定义业务域名

def get_iplist(domain=""):	#域名解析函数，解析成功IP将被追加到iplist
	try:
		A = dns.resolver.query(domain, 'A')	#解析A记录类型
	except Exception as e:
		print ("dns resolver error: ")+str(e)
		return
	for i in A.response.answer:
		for j in i.items:
			iplist.append(j.address)	#追加到iplist
	return True

def checkip(ip):
	checkurl = ip+":80"
	getcontent = ""
	http.client.socket.setdefaulttimeout(5)		#定义http连接超时时间（5秒）
	conn = http.client.HTTPConnection(checkurl)	#创建http连接对象

	try:
		conn.request("GET", "/", headers = {"Host": appdomain})		#发起url请求，添加host主机头

		r = conn.getresponse()
		getcontent = r.read(15)		#获取url页面前15个字符，以便做可用性校验
	finally:
		if getcontent == "<!doctype html>":	#监控URL页的内容一般是事先定义好的，比如"HTTP200"等

			print (ip+" [OK]")
		else:
			print (ip+" [Error]")	#此处可放告警程序，可以是邮件、短信通知

if __name__ == "__main__":
	if get_iplist(appdomain) and len(iplist)>0:	#条件：域名解析正确且至少返回一个IP
		for ip in iplist:
			checkip(ip)
	else:
		print ("dns resolver error.")