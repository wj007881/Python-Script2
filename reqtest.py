import requests as req
import pytest
class Test_api():
    def tear_down(self):
        print("end")

    def setUp(self):
        print("start")


    def test1(self):
        url="http://baidu.com"
        print(req.get(url).history)
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
    pass