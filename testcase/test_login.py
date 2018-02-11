# -*- coding:utf-8 -*-
# Aothor:Lin

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest, time
from page.login import login


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
        self.driver.quit ()

    @staticmethod
    def suite():
        suit = unittest.TestSuite ( unittest.makeSuite ( Login ) )
        return suit


if __name__ == '__main__':
    unittest.TextTestRunner ( verbosity=2 ).run ( Login.suite () )
