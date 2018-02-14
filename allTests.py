# -*- coding:utf-8 -*-
# Aothor:Lin
import unittest, os, sys, HTMLTestRunner, time


def suite():
    test_dir = "G:/caolinlin/zidonghua/RLtestdemo/Testcase"
    dir_case = unittest.defaultTestLoader.discover (
        test_dir,
        pattern="test_*.py",
        top_level_dir=None
    )
    return dir_case


def getNowTime():
    return time.strftime ( "%Y-%m-%d_%H-%M-%S", time.localtime ( time.time () ) )


def runAutomation():
    filename = u"G:\\caolinlin\\zidonghua\\JRLtestdemo\\Report\\" + getNowTime () + "_TestReort.html"
    fp = file ( filename, 'wb' )
    runner = HTMLTestRunner.HTMLTestRunner (
        stream=fp,
        title=u"自动化测试报告",
        description=u"用例执行情况："
    )
    runner.run ( suite () )


if __name__ == '__main__':
    runAutomation ()
