# -*- coding:utf-8 -*-
# Aothor:Lin

import unittest
import ddt
from selenium import webdriver
from Page import basetestcase
from Page.BasePage import browser
from Model.data import ExcelUtil
from Page.login import LoginPage
from Page.quit import QuitPage
from Page.Apply_for_loan import Apply_for_loan
from Model.logger import Log
from Page.basetestcase import BaseTestCase, AppTestCase

# log = Log ()

filePath = (u'G:\\cll\\zidonghua\\JRLtestdemo\\Data-Driven\\Login_data.xlsx')
data = ExcelUtil ()
testData = data.dict_data ( filePath )
print ( testData )


@ddt.ddt
class Instantiation_apply_for_loan ( unittest.TestCase ):
    @classmethod
    def setUpClass(cls):
        cls.driver = browser ( "chrome" )
        cls.driver.maximize_window ()
        cls.driver.implicitly_wait ( 20 )
        cls.base_url = ('http://testnew.ruilongjin.com')
        cls.verificationErrors = []
        cls.accept_next_alert = True
        cls.login = LoginPage ( cls.driver )
        cls.Quit = QuitPage ( cls.driver )
        cls.loan = Apply_for_loan ( cls.driver )

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit ()
        cls.verificationErrors = []
        # cls.assertEqual ( [],cls.verificationErrors)

    @ddt.data ( *testData )
    def test_apply_for_loan(self, data):
        # log.info ( u"---测试开始----" )
        # print(data)
        # log.info ( u"---输入账号----" )
        self.driver.get ( self.base_url + "/login" )
        # log.info ( u"---输入密码----" )
        self.login.login ( data["name"], data["pswd"] )
        # log.info ( u"---判断登录后的URL是否与登录前相同----" )
        self.assertTrue ( self.base_url + 'front/account/home?login=1', self.driver.current_url )
        # log.info ( u"---退出登录----" )
        print ( data["per_name"] )
        self.loan.apply_for_loan ( data["per_name"], data["phone"], data["value1"], data["value2"], data["address"],
                                   data["value3"], data["value4"], data["value5"], data["amount"], data["dead"],
                                   data["value6"], data["descs"] )
        self.Quit.quit ()
        # log.info ( u"---测试结束----" )


if __name__ == '__main__':
    testunit = unittest.TestSuite ()
    testunit.addTest ( unittest.makeSuite ( Instantiation_apply_for_loan ) )
