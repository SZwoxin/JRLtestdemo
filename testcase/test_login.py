# -*- coding:utf-8 -*-
# Aothor:Lin
import unittest

import ddt
from selenium import webdriver

from Model.data import ExcelUtil
from Page.login import login
from Page.quit import quit

filePath = (u'G:\\caolinlin\\zidonghua\\JRLtestdemo\\Data-Driven\\Login_data.xlsx')
sheetName = "Sheet1"
data = ExcelUtil ( filePath, sheetName )
testData = data.dict_data ()


# print testData

@ddt.ddt
class Login ( unittest.TestCase ):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome ()
        cls.driver.maximize_window ()
        cls.driver.implicitly_wait ( 30 )
        cls.base_url = ('http://pctest.ruilongjin.com')
        cls.verificationErrors = []
        cls.accept_next_alert = True

    @ddt.data ( *testData )
    def test_login(self, data):
        driver = self.driver
        driver.get ( self.base_url + "/login" )
        login ( self, data["name"], data["pswd"] )
        self.assertTrue ( self.base_url + 'front/account/home?login=1', self.driver.current_url )
        quit ( self )

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit ()
        # cls.assertEqual ( [],cls.verificationErrors)


if __name__ == '__main__':
    testunit = unittest.TestSuite ()
    testunit.addTest ( unittest.makeSuite ( Login ) )
'''
    # unittest.TextTestRunner ( verbosity=2 ).run ( testunit )
    now = time.strftime ( "%Y-%m-%d_%H-%M-%S", time.localtime(time.time()) )
    filename = u"G:\\"+now+"TestReport.html"
    fp = file(filename,'wb')
    with open(filename, 'wb') as fp:
        runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title=u'自动化测试报告', description=u'用例执行详情：')
        runner.run(testunit)
        fp.close ()
'''