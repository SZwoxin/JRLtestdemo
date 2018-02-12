# -*- coding:utf-8 -*-
# Aothor:Lin
from selenium import webdriver
import unittest
import HTMLTestRunner
import xlrd, sys
from time import sleep


class LoadBaiduSearchTestData:
    def __int__(self, path):
        self.path = path

    def load_data(self):
        # 打开excel文件
        excel = xlrd.open_workbook ( self.path )
        # 获取第一个工作表
        table = excel.sheets ()[0]
        # 获取行数
        nrows = table.nrows
        # 从第二行开始遍历数据
        # 存入一个list中
        test_data = []
        for i in range ( 1, nrows ):
            test_data.append ( table.row_values ( i ) )
        # 返回读取的数据列表
        return test_data
