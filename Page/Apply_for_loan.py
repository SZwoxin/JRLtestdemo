# -*- coding:utf-8 -*-
# Aothor:Lin

from Page.BasePage import page


class Apply_for_loan ( page ):
    top_goto_loan_loc = ('id', 'top-goto-loan')
    per_name_input_loc = ('id', 'per_name_input')
    phone_loc = ('id', 'phone')
    provinces_id_loc = ('id', 'provinces_id')
    city_loc = ('id', 'city')
    address_loc = ('id', 'address')
    pro_loc = ('id', 'pro')
    proType_loc = ('id', 'proType')
    pawn_id_loc = ('id', 'pawn_id')
    amount_loc = ('id', 'amount')
    dead_loc = ('id', 'dead')
    deadlineType_loc = ('id', 'deadlineType')
    descs_loc = ('name', 'descs')
    submit_bot_loc = ('id', 'submit_bot')

    def loan(self):
        self.click ( self.top_goto_loan_loc )

    def input_per_name(self, per_name):
        self.send_keys ( self.per_name_input_loc, per_name )

    def input_phone(self, phone):
        self.send_keys ( self.phone_loc, phone )

    def provinces_id(self, value1):
        self.select_by_value ( self.provinces_id_loc, value1 )

    def city(self, value2):
        self.select_by_value ( self.city_loc, value2 )

    def input_address(self, address):
        self.send_keys ( self.address_loc, address )

    def pro(self, value3):
        self.select_by_value ( self.pro_loc, value3 )

    def proType(self, value4):
        self.select_by_value ( self.proType_loc, value4 )

    def pawn_id(self, value5):
        self.select_by_value ( self.pawn_id_loc, value5 )

    def input_amount(self, amount):
        self.send_keys ( self.amount_loc, amount )

    def input_dead(self, dead):
        self.send_keys ( self.dead_loc, dead )

    def deadlineType(self, value6):
        self.select_by_value ( self.deadlineType_loc, value6 )

    def input_descs(self, descs):
        self.send_keys ( self.descs_loc, descs )

    def submit_bot(self):
        self.click ( self.submit_bot_loc )

    def apply_for_loan(self, per_name, phone, value1, value2, address, value3, value4, value5, amount, dead, value6,
                       descs):
        self.loan ()
        self.input_per_name ( per_name )
        self.input_phone ( phone )
        self.provinces_id ( value1 )
        self.city ( value2 )
        self.input_address ( address )
        self.pro ( value3 )
        self.proType ( value4 )
        self.pawn_id ( value5 )
        self.input_amount ( amount )
        self.input_dead ( dead )
        self.deadlineType ( value6 )
        self.input_descs ( descs )
        self.submit_bot ()
