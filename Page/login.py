# -*- coding:utf-8 -*-
# Aothor:Lin

def login(self):
    driver = self.driver
    driver.find_element_by_id ( "name" ).clear ()
    driver.find_element_by_id ( "name" ).send_keys ( '15011228811' )
    driver.find_element_by_id ( "password" ).clear ()
    driver.find_element_by_id ( "password" ).send_keys ( 'q12345' )
    driver.find_element_by_id ( "login_submit" ).click ()
