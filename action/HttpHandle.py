import requests
class HttpHandle():
    def __init__(self):
        self.session=requests.Session()
        self.session_id=requests.session

    def visit(self,url,method="get",params=None,data=None,json=None,**kwargs):
        """
        :param url: 请求地址
        :param method: 请求方法
        :param params: get参数
        :param data: data参数
        :param json: json参数
        :return:返回请求的json数据
        """
        if method.upper()=="GET":
            try:
                res=self.session.get(url,params=params)
            except Exception as e:
                print("Get Error, Because %s".format(e))
        elif method.upper()=="POST":
            try:
                res=self.session.post(url,params=params,data=data,json=json,**kwargs)
            except Exception as e:
                print("Post Error, Because %s".format(e))
        elif method.upper()=="DEL":
            try:
                res=self.session.delete(url,params=params,data=data,json=json,**kwargs)
            except Exception as e:
                print("Post Error, Because %s".format(e))
        try:
            return res
        except Exception as e:
            print("Bad Request, Because %s".format(e))

    def get_cookie(self):
        """
        返回cookie数据
        """
        try:
            return self.cookies()
        except Exception as e:
            print("Not Cookie, Because %s".format(e))

    def get_json(self):
        """
        返回cookie数据
        """
        try:
            return self.json()
        except Exception as e:
            print("Not Json, Because %s".format(e))
