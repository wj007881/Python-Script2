# -*- coding:utf-8 -*-
"""
@software: PyCharm
@file: ddns.py
@time: 2021/9/22 14:02
@author: Ryan
"""
import socket

from flask import Flask,request,jsonify
from flask_cors import *

app = Flask(__name__)
CORS(app, supports_credentials=True)  # 设置跨域
@app.route('/set_ip',methods=["POST"])
def set_ip():
    data=request.json
    ip=data['ip']
    try:
        f=open(r'./ip.txt','w')
        f.write(ip)
        f.close()
    except:
        return jsonify({"msg": "ERROE"})
    return jsonify({"msg":"OK","ip": ip})
@app.route('/get_ip')
def get_ip():
    f = open(r'./ip.txt', 'r')
    ip = f.readline()
    return jsonify({"msg":"OK","ip": ip})
if __name__ == "__main__":
    hostname = socket.gethostname()
    # 获取本机ip
    ip = socket.gethostbyname(hostname)
    # ip=get_host_ip()
    app.debug = True
    app.run(host=ip,port=5000)
