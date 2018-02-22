# -*- coding:utf-8 -*-
# Aothor:Lin
import os, unittest, time, smtplib
from Model import HTMLTestRunner
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage


# 定义测试报告路径
def suite():
    test_dir = os.path.join ( os.getcwd (), "Testcase" )
    # test_dir =path
    # test_dir ="G:\\caolinlin\\zidonghua\\JRLtestdemo\\Testcase"
    dir_case = unittest.defaultTestLoader.discover (
        test_dir,
        pattern="test_*.py",
        top_level_dir=None
    )
    return dir_case


#生成测试报告时间
def getNowTime():
    return time.strftime ( "%Y-%m-%d_%H-%M-%S", time.localtime ( time.time () ) )


#定义测试报告存放路径与报告名称
def runAutomation():
    filename = u"G:\\caolinlin\\zidonghua\\JRLtestdemo\\Report\\" + getNowTime () + "_TestReort.html"
    fp = file ( filename, 'wb' )
    runner = HTMLTestRunner.HTMLTestRunner (
        stream=fp,
        title=u"自动化测试报告",
        description=u"用例执行情况："
    )
    runner.run ( suite () )


def sentmail(file_new):
    mail_from = '469551994@qq.com'
    mail_to = '1243054080@qq.com'
    _pswd = '输入授权码'
    f = open ( file_new, 'rb' )
    mail_body = f.read ()
    f.close ()
    msg = MIMEText ( mail_body, _subtype='html', _charset='utf-8' )
    msg['Subject'] = u'自动化测试报告'
    msg['date'] = time.strftime ( '%a, %d %b %Y %H:%M:%S %z' )
    # smtp = smtplib.SMTP ()
    s = smtplib.SMTP_SSL ( 'smtp.qq.com', 465 )
    s.login ( mail_from, _pswd )
    s.sendmail ( mail_from, mail_to, msg.as_string () )
    s.quit ()
    print u'邮件发送成功!'


def sendreport():
    result_dir = 'G:\\caolinlin\\zidonghua\\JRLtestdemo\\Report'
    lists = os.listdir ( result_dir )
    lists.sort ( key=lambda fn: os.path.getmtime ( result_dir + "\\" + fn ) if not os.path.isdir (
        result_dir + "\\" + fn ) else 0 )
    print (u'最新测试生成的报告：' + lists[-1])
    file_new = os.path.join ( result_dir, lists[-1] )
    print file_new
    sentmail ( file_new )

if __name__ == '__main__':
    runAutomation ()
    sendreport ()
