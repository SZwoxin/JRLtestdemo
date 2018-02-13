# -*- coding:utf-8 -*-
# Aothor:Lin

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from Model.data import ExcelUtil
import ddt


def login(self, name, pswd):
    driver = self.driver
    driver.find_element_by_id ( "name" ).clear ()
    driver.find_element_by_id ( "name" ).send_keys ( name )
    driver.find_element_by_id ( "password" ).clear ()
    driver.find_element_by_id ( "password" ).send_keys ( pswd )
    driver.find_element_by_id ( "login_submit" ).click ()
