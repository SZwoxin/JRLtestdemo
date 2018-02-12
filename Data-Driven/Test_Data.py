# -*- coding:utf-8 -*-
# Aothor:Lin
import xlrd


def login_data():
    excel = xlrd.open_workbook ( u'G:\\caolinlin\\zidonghua\\JRLtestdemo\\Data-Driven\\Login_data.xlsx' )
    table = excel.sheets ()[0]
    nrows = table.nrows
    data = []
    for i in range ( 1, nrows ):
        data.append ( table.row_values ( i ) )
    # print data[-1]
    return data[-1]

# print login_data()
