#!python3
#coding:utf-8

'''
################################
@ MyBlog: blog.csdn.net/hjxzt1
          www.mykurol.com
  github: https://github.com/kurolz
################################

    爬取集思录网站债券数据
    目前可存为txt或xlsx两种格式
    超过定义的涨幅或跌幅，可邮件通知
    #### 请填写发送的邮箱密码 ####
'''



'''邮件通知'''
def sendMail(id,uplift):
    import smtplib
    from email.mime.text import MIMEText
    from email.header import Header

    # 第三方 SMTP 服务
    mail_host = "smtp.163.com"  # 设置smtp服务器，例如：smtp.163.com
    mail_user = "kurolz@163.com"  # 发送的邮箱用户名
    mail_pass = "******"  # 发送的邮箱密码

    sender = 'kurolz@163.com'  # 发送的邮箱
    receivers = 'kurolz@163.com'  # 接收的邮箱
    if uplift < format(0, '.0%'):  # uplift为涨幅或跌幅
        text = '债券代码：' + id + ', 跌幅为：' + uplift
    else:
        text = '债券代码：' + id + ', 涨幅为：' + uplift  # 发送的文本
    message = MIMEText(text)
    message['From'] = sender
    message['To'] = receivers

    subject = text
    message['Subject'] = Header(subject)

    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
        smtpObj.login(mail_user, mail_pass)    # login
        smtpObj.sendmail(sender, receivers, message.as_string())    # 发送邮件
        print("邮件发送成功")
    except smtplib.SMTPException as e:
        print("Error: 无法发送邮件" + str(e))

'''当债券涨幅超过定义的limit值时，发送邮件通知'''
def limitsendMail(limit,i,data):
    if limit < 0:
        if data < format(0, '.0%'):
            limit = format(limit, '.3%')
            if data.split('-')[1] > limit.split('-')[1]:
                sendMail(i, data)
    else:
        limit = format(limit, '.0%')
        if data > limit:
            sendMail(i, data)

'''定义抓取数据的行'''
def data_row():
    jisilu_id = []  # 要爬取的债券代码
    p = 0   # 可选，0为取双行，-1为取单行

    while True:
        try:
            p += 2  # 可选，2为取单双行，1位取所有行
            p = str(p)  # 转换为str，用于抓取数据
            element = driver.find_element_by_xpath('//*[@id="flex3"]/tbody/tr['+ p +']')
            data_id = element.get_attribute("id")   # 抓取所有需要爬取的债券代码
            p = int(p)  # 转换为int，维持增量循环
        except:
            break
        jisilu_id.append(data_id)
    return jisilu_id

'''定义抓取数据的列'''
def data_colum():
    c = []  # 存储要抓取的列
    for num in range(1,24):
        c.append(str(num))
    # 删除三个无关数据的列
    del c[20]
    del c[12]
    del c[11]
    return c

'''定义爬取的操作'''
try:
    from selenium import webdriver
    import ssl

    html = 'https://www.jisilu.cn/data/cbnew/#tlink_3'  # 定义爬取的网站
    ssl._create_default_https_context = ssl._create_unverified_context  # 取消证书认证
    try:
        driver = webdriver.PhantomJS()
        driver.get(html)
        driver.implicitly_wait(3)  # 等待3秒
    except:
        print ('请安装phantomjs')

except ImportError:
    print ('No module named selenium. 请安装selenium模块')


'''抓取数据'''
a = {}  # 存储数据，存储格式：a = {债券代码:{title:data,title:data, ...}, ...}
for i in data_row():
    b = {}  # 存储格式：b = {title：data, ...}
    for lie in data_colum():
        title = driver.find_element_by_xpath('//*[@id="flex3"]/thead/tr[2]/th['+lie+']').text   # 抓取title
        data = driver.find_element_by_xpath('//*[@id='+i+']/td['+lie+']').text  # 抓取数值
        title = title.replace("\n", "") # 去掉title中的换行符
        b[title] = data
        if lie == "4":
            limitsendMail(0.05, i, data)
    a[i] = b


'''数据输出保存'''
class print_data(object):
    def __init__(self, filename):
        self.filename = filename

    '''输出到TXT'''
    def printTxt(self):
        import time
        with open(self.filename, 'ab+') as w:
            nowtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            w.write(("\n@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ " + nowtime + " @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n").encode())
        w.close()
        for key in a:
            for key2 in a[key]:
                with open(self.filename, 'ab+') as w:
                    w.write((key2 + ":" + a[key][key2] + "，").encode('utf-8'))
                w.close()
            with open(self.filename, 'ab+') as w:
                w.write(("\n").encode())
            w.close()

    '''输出到Xlsx'''
    def printXlsx(self):
        try:
            import xlsxwriter
            workbook = xlsxwriter.Workbook(self.filename)  # 创建一个Excel文件
            worksheet = workbook.add_worksheet()  # 创建一个工作表对象

            colum_len = ''
            for key in a:
                colum_len = key
                if colum_len != '':
                    break

            '''写入title'''
            colum_num = 0
            while (colum_num < len(a[colum_len].keys())):
                for i in list(a[colum_len].keys()):
                    worksheet.write(0, colum_num, i)  # 写入行列表示法的单元格
                    colum_num += 1

            '''写入数值'''
            row_num = 1
            colum_num_2 = 0
            while (colum_num_2 < len(a[colum_len].keys())):
                for key in a:
                    colum_num_2 = 0
                    for key2 in a[key]:
                        worksheet.write(row_num, colum_num_2, a[key][key2])  # 写入行列表示法的单元格
                        colum_num_2 += 1
                    row_num += 1

        except ImportError:
            print ('No module named xlsxwriter，输出为xlsx文件需要安装xlsxwriter模块，或重新定义输出为txt文件')

if __name__ == "__main__":
    printfilename = '07150240-2.xlsx'
    file = print_data(printfilename)
    if printfilename.split('.')[1] == 'xlsx':
        file.printXlsx()
    elif printfilename.split('.')[1] == 'txt':
        file.printTxt()
    else:
        print ('输出文件名定义错误，无法输出，只能为xlsx或txt格式')
