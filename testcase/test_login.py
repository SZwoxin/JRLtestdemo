# -*- coding:utf-8 -*-
# Aothor:Lin

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest, time
from page.login import login
from page.quit import quit
from Report import HTMLTestRunner
class Login ( unittest.TestCase ):
    def setUp(self):
        self.driver = webdriver.Chrome ()
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
    now = time.strftime ( "%Y-%m-%M-%H_%M_%S", time.localtime ( time.time () ) )
    filename = "G:\\caolinlin\\zidonghua\\JRLtestdemo\\Report\\"
    fp = file ( filename + u"金瑞龙" + now + ".html", 'wb' )
    runner = HTMLTestRunner.HTMLTestRunner ( stream=fp, title=u"金瑞龙测试", description=u"测试结果" )
    runner.run ( testunit )
    fp.close ()
