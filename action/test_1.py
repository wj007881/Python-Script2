# -*- coding: utf-8 -*-
#author:Ryan
#time  :2021/3/11

import requests as req
import unittest
class Test_api(unittest.TestCase):

    @classmethod
    def setUpClass(self) -> None:
        print("start")

    @classmethod
    def tearDownClass(self) -> None:
        print("end")

    def test1(self):
        url="http://baidu.com"
        print("History",req.get(url).history)
        url="http://bilibili.com"
        bilibili=req.get(url)
        cookie=bilibili.cookies
        bilibili2=req.post(url,cookies=cookie)
        print(bilibili2.request)

    def test2(self):
        print(req.session)
        url="http://baidu.com"
        print(req.get(url))

if __name__=="__main__":
    unittest.main()