# -*- coding:utf-8 -*-
# Aothor:Lin

from selenium import webdriver
from selenium.webdriver.common.by import By
from BasePage import Page
import unittest


class login ( unittest.TestCase ):
    def setUp(self):
        self.driver = webdriver.Chrome ()
        self.driver.maximize_window ()
        self.driver.implicitly_wait ( 30 )
        self.driver.get ( 'http://pctest.ruilongjin.com' )

    def test_001(self):
        self.assertEqual ( u'【金瑞龙官网】银行存管p2p网络借贷互联网金融服务平台', self.driver.title )
        self.driver.quit ()

    @staticmethod
    def suite():
        suit = unittest.TestSuite ( unittest.makeSuite ( login ) )
        return suit


if __name__ == '__main__':
    unittest.TextTestRunner ( verbosity=2 ).run ( login.suite () )
