# -*- coding:utf-8 -*-
# Aothor:Lin

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time as t


def wait():
    t.sleep ( 2 )


def clickLogin(driver):
    wait ()
