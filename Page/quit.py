# -*- coding:utf-8 -*-
# Aothor:Lin

from Page.BasePage import page


class QuitPage ( page ):
    login_loc = ('id', 'login')

    def quit(self):
        self.click ( self.login_loc )
