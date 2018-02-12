# -*- coding:utf-8 -*-
# Aothor:Lin

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException


def login(self, name, psd):
    driver = self.driver
    driver.find_element_by_id ( "name" ).clear ()
    driver.find_element_by_id ( "name" ).send_keys ( name )
    driver.find_element_by_id ( "password" ).clear ()
    driver.find_element_by_id ( "password" ).send_keys ( psd )
    driver.find_element_by_id ( "login_submit" ).click ()
