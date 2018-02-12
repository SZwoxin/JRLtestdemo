# -*- coding:utf-8 -*-
# Aothor:Lin

from selenium import webdriver
import sys, xlrd

reload ( sys )
import unittest
from Page.login import login
from Page.quit import quit
from Report import HTMLTestRunner
class Login ( unittest.TestCase ):
    def setUp(self):
        self.driver = webdriver.Chrome ()
        self.driver.maximize_window ()
        self.driver.implicitly_wait ( 30 )
        self.base_url = ('http://pctest.ruilongjin.com')
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_login(self):
        driver = self.driver
        driver.get ( self.base_url + "/login" )
        login ( self )
        self.assertTrue ( self.base_url + 'front/account/home?login=1', self.driver.current_url )
        quit ( self )

    def tearDown(self):
        self.driver.quit ()
        self.assertEqual ( [], self.verificationErrors )


if __name__ == 'test_login':
    testunit = unittest.TestSuite ()
    testunit.addTest ( unittest.makeSuite ( Login.test_login ) )
    unittest.TextTestRunner ( verbosity=2 ).run ( testunit )
'''   now = time.strftime ( "%Y-%m-%M-%H_%M_%S", time.localtime ( time.time () ) )
    filename = "G:/test.html"
    with open(filename, 'wb') as fp:
        runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title=u'测试', description=u'用例执行详情：')
        runner.run(testunit)
        fp.close ()
'''
