# -*- coding:utf-8 -*-
# Aothor:Lin

from Model.E_email import sendreport
from Model.report import runAutomation
from selenium import webdriver





if __name__ == '__main__':
    # 调用测试报告
    runAutomation ()
    # 调用邮件发送
    # sendreport ()
