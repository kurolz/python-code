#!python
# -*- coding: UTF-8 -*-

'''
SMTP（Simple Mail Transfer Protocol）即简单邮件传输协议,它是一组用于由源地址到目的地址传送邮件的规则，由它来控制信件的中转方式。
python的smtplib提供了一种很方便的途径发送电子邮件。它对smtp协议进行了简单的封装。

'''


import smtplib
from email.mime.text import MIMEText
from email.header import Header

# 第三方 SMTP 服务
mail_host = "smtp.163.com"  # 设置smtp服务器，例如：smtp.163.com
mail_user = "******@163.com"  # 用户名
mail_pass = "****"  # 口令

sender = '******@163.com'   # 发送邮件
receivers = '******@qq.com'  # 接收邮件

message = MIMEText('This is a Python Test Text')
message['From'] = sender
message['To'] = receivers

subject = 'One Test Mail'
message['Subject'] = Header(subject)

try:
    smtpObj = smtplib.SMTP()
    smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
    smtpObj.login(mail_user, mail_pass)
    smtpObj.sendmail(sender, receivers, message.as_string())
    print ("邮件发送成功")
except smtplib.SMTPException as e:
    print ("Error: 无法发送邮件"+str(e))