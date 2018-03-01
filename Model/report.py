# -*- coding:utf-8 -*-
# Aothor:Lin
import os, unittest, time
from Model import HTMLTestRunner


# 定义测试报告路径
def suite():
    test_dir = os.path.join ( os.getcwd (), "Testcase" )
    # test_dir =path
    # test_dir ="G:\\cll\\zidonghua\\JRLtestdemo\\Testcase"
    dir_case = unittest.defaultTestLoader.discover (
        test_dir,
        pattern="test_*.py",
        top_level_dir=None
    )
    return dir_case


# 生成测试报告时间
def getNowTime():
    return time.strftime ( "%Y-%m-%d_%H-%M-%S", time.localtime ( time.time () ) )


# 定义测试报告存放路径与报告名称
def runAutomation():
    filename = u"G:\\cll\\zidonghua\\JRLtestdemo\\Report\\" + getNowTime () + "_TestReort.html"
    fp = file ( filename, 'wb' )
    runner = HTMLTestRunner.HTMLTestRunner (
        stream=fp,
        title=u"自动化测试报告",
        description=u"用例执行情况：",
        verbosity=2,
        # retry=2
    )
    runner.run ( suite () )
