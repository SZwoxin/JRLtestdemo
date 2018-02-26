# -*- coding:utf-8 -*-
# Aothor:Lin

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from Page.basetestcase import BaseTestCase, AppTestCase
from Page.BasePage import page

'''    
    ID = "id"
    XPATH = "xpath"
  LINK_TEXT = "link text"
  PARTIAL_LINK_TEXT = "partial link text"
  NAME = "name"
  TAG_NAME = "tag name"
  CLASS_NAME = "class name"
   CSS_SELECTOR = "css selector"
'''


class LoginPage ( page ):
    useName_loc = ('id', 'name')
    passWord_loc = ('id', 'password')
    login_loc = ('id', 'login_submit')

    def input_name(self, name):
        self.send_keys ( self.useName_loc, name )

    def input_pswd(self, pswd):
        self.send_keys ( self.passWord_loc, pswd )

    def click_submit(self):
        self.click ( self.login_loc )

    def login(self, name, pswd):
        self.input_name ( name )
        self.input_pswd ( pswd )
        self.click_submit ()
