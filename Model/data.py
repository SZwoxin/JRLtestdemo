# -*- coding:utf-8 -*-
# Aothor:Lin

# coding:utf-8
import xlrd
import json


class ExcelUtil:
    def dict_data(self, excel_path):
        self.data = xlrd.open_workbook ( excel_path )
        self.table_list = self.data.sheet_names ()
        # print(self.table_list)
        self.sheetNum = len ( self.table_list )
        # print(self.sheetNum)
        r = []
        for i in range ( self.sheetNum ):
            self.readName = self.table_list[i]
            # print(self.readName)
            self.table = self.data.sheet_by_name ( self.readName )
            # print(self.table)
            # 获取总行数
            self.rowNum = self.table.nrows
            # print(self.rowNum)
            # 获取总列数
            self.colNum = self.table.ncols
            # print(self.colNum)
            if self.rowNum <= 1:
                print ( "总行数小于1" )
            else:
                j = 1
                for i in range ( self.rowNum - 1 ):
                    s = {}
                    # 从第二行取对应values值
                    self.values = self.table.row_values ( j )
                    # print(self.values )
                    # 获取第一行作为key值
                    self.keys = self.table.row_values ( 0 )
                    # print(self.keys)
                    # print(self.values,self.keys)
                    for x in range ( self.colNum ):
                        s[self.keys[x]] = self.values[x]
                    r.append ( s )
                    j += 1
                    # return json.dumps ( r ).decode ( "unicode-escape" )
                    # print(x)
        return r
'''
if __name__ == "__main__":
    filePath = (u'G:\\cll\\zidonghua\\JRLtestdemo\\Data-Driven\\Login_data.xlsx')
    sheetName = "Sheet1"
    data = ExcelUtil ( filePath, sheetName )
    print (data.dict_data ())
'''
