# -*- coding:utf-8 -*-
# Aothor:Lin

import unittest
from selenium import webdriver
from Page.BasePage import browser


class BaseTestCase ( unittest.TestCase ):
    def setUp(self):
        self.driver = browser ()
        self.driver.maximize_window ()
        self.driver.implicitly_wait ( 30 )

    def tearDown(self):
        self.driver.quit ()


class AppTestCase ( unittest.TestCase ):
    def setUp(self):
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = '4.4.4'
        desired_caps['deviceName'] = 'Samsung Galaxy S4-4.4.4'
        desired_caps['appPackage'] = 'com.taobao.mobile.dipei'
        desired_caps['appActivity'] = 'com.taobao.ecoupon.activity.PortalActivity'
        self.driver = webdriver.Remote ( "http://127.0.0.1:4723/wd/hub", desired_caps )

    def tearDown(self):
        self.driver.quit ()


if __name__ == '__main__':
    unittest.main ()
