# -*- coding:utf-8 -*-
# Aothor:Lin
from selenium import webdriver
import ddt, time
import unittest
from Page.login import login
from Page.quit import quit
from Model.data import ExcelUtil
from Report import HTMLTestRunner

filePath = (u'G:\\caolinlin\\zidonghua\\JRLtestdemo\\Data-Driven\\Login_data.xlsx')
sheetName = "Sheet1"
data = ExcelUtil ( filePath, sheetName )
testData = data.dict_data ()


# print testData

@ddt.ddt
class Login ( unittest.TestCase ):
    def setUp(self):
        self.driver = webdriver.Chrome ()
        self.driver.maximize_window ()
        self.driver.implicitly_wait ( 30 )
        self.base_url = ('http://pctest.ruilongjin.com')
        self.verificationErrors = []
        self.accept_next_alert = True

    @ddt.data ( *testData )
    def test_login(self, data):
        driver = self.driver
        driver.get ( self.base_url + "/login" )
        login ( self, data["name"], data["pswd"] )
        self.assertTrue ( self.base_url + 'front/account/home?login=1', self.driver.current_url )
        quit ( self )

    def tearDown(self):
        self.driver.quit ()
        self.assertEqual ( [], self.verificationErrors )


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
