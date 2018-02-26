# -*- coding:utf-8 -*-
# Aothor:Lin
import unittest

import ddt
from selenium import webdriver
from Page import basetestcase
from Page.BasePage import browser
from Model.data import ExcelUtil
from Page.login import LoginPage
from Page.quit import quit
from Model.logger import Log
from Page.basetestcase import BaseTestCase, AppTestCase


# log = Log ()

filePath = (u'G:\\caolinlin\\zidonghua\\JRLtestdemo\\Data-Driven\\Login_data.xlsx')
sheetName = "Sheet1"
data = ExcelUtil ( filePath, sheetName )
testData = data.dict_data ()


# print testData

@ddt.ddt
class Login ( unittest.TestCase ):
    @classmethod
    def setUpClass(cls):
        cls.driver = browser ( "chrome" )
        cls.driver.maximize_window ()
        cls.driver.implicitly_wait ( 30 )
        cls.base_url = ('http://pctest.ruilongjin.com')
        cls.verificationErrors = []
        cls.accept_next_alert = True
        cls.login = LoginPage ( cls.driver )
    @classmethod
    def tearDownClass(cls):
        cls.driver.quit ()
        cls.verificationErrors = []
        # cls.assertEqual ( [],cls.verificationErrors)

    @ddt.data ( *testData )
    def test_login(self, data):
        #log.info ( u"---测试开始----" )
        #log.info ( u"---输入账号----" )
        self.driver.get ( self.base_url + "/login" )
        #log.info ( u"---输入密码----" )
        self.login.login ( data["name"], data["pswd"] )
        #log.info ( u"---判断登录后的URL是否与登录前相同----" )
        self.assertTrue ( self.base_url + 'front/account/home?login=1', self.driver.current_url )
        #log.info ( u"---退出登录----" )
        quit ( self )
        #log.info ( u"---测试结束----" )




if __name__ == '__main__':
    testunit = unittest.TestSuite ()
    testunit.addTest ( unittest.makeSuite ( Login ) )
