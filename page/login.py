# -*- coding:utf-8 -*-
# Aothor:Lin
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest, time


def login(self):
    driver = self.driver
    driver.maximize_window ()
    driver.find_element_by_id ( "name" ).clear ()
    driver.find_element_by_id ( "name" ).send_keys ( '15011228811' )
    driver.find_element_by_id ( "password" ).clear ()
    driver.find_element_by_id ( "password" ).send_keys ( 'q12345' )
    driver.find_element_by_id ( "login_submit" ).click ()
