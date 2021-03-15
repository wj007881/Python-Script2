# -*- coding: utf-8 -*-
#author:Ryan
#time  :2021/3/11
import unittest,os
testloder=unittest.TestLoader()
#测试用例地址
dir_path=os.path.dirname(os.path.abspath(__file__))
case_path=os.path.join(dir_path,"action")
suite=testloder.discover(start_dir=case_path)


#报告地址
report_path=os.path.join(dir_path,"report")
file_path=os.path.join(report_path,"Test_report.txt")
if not os.path.exists(report_path):
	os.mkdir(report_path)
if not os.path.exists(file_path):
	open(file_path,"w")

with open(file_path,"w",encoding="utf-8") as f:
	runner=unittest.TextTestRunner(f,verbosity=2)
	#运行测试用例
	runner.run(suite)


