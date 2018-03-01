# -*- coding:utf-8 -*-
# Aothor:Lin
import os, time, smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import yagmail


# 定义发送邮件
def sentmail(file_new):
    # 配置信息
    _mail_from = '登录邮箱'
    _mail_to = ['发送邮箱']
    _pswd = '登录密码'
    _mail_server = '邮箱服务器'
    _port = '邮箱端口'
    # 定义正文
    f = open ( file_new, 'rb' )
    mail_body = f.read ()
    f.close ()

    msg = MIMEMultipart ()
    # 定义标题
    # msgg = MIMEText ( mail_body, _subtype='html', _charset='utf-8' )
    msg['Subject'] = u'自动化测试报告'
    # 定义发送时间
    msg['date'] = time.strftime ( '%a, %d %b %Y %H:%M:%S %z' )
    # 定义发送人
    msg['from'] = _mail_from
    # 定义接收人
    msg['to'] = ";".join ( _mail_to )
    # 正文
    body = MIMEText ( mail_body, _subtype='html', _charset='utf-8' )
    msg.attach ( body )
    # 附件
    att = MIMEText ( mail_body, _subtype='html', _charset='utf-8' )
    att["Content-Type"] = "application/octet-stream"
    att["Content-Disposition"] = 'attachment;filename = "test_report.html'
    msg.attach ( att )
    # smtp = smtplib.SMTP ()
    # smtp.connect(mail_server,port)
    # 定义SSL第三方QQ登录方式
    s = smtplib.SMTP_SSL ( _mail_server, _port )
    # 登录信息
    s.login ( _mail_from, _pswd )
    # 执行发送
    s.sendmail ( _mail_from, _mail_to, msg.as_string () )
    s.quit ()
    print u'邮件发送成功!'


# 定义邮件路径与命名
def sendreport():
    result_dir = 'G:\\cll\\zidonghua\\JRLtestdemo\\Report'
    lists = os.listdir ( result_dir )
    lists.sort ( key=lambda fn: os.path.getmtime ( result_dir + "\\" + fn ) if not os.path.isdir (
        result_dir + "\\" + fn ) else 0 )
    print (u'最新测试生成的报告：' + lists[-1])
    file_new = os.path.join ( result_dir, lists[-1] )
    print file_new
    sentmail ( file_new )
