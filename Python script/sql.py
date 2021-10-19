# -*- coding: utf-8 -*-
# author: Ryan
# time: 2021/9/7
import json
import time

from flask_sqlalchemy import SQLAlchemy
import pymysql
from flask import Flask, send_file, request, send_from_directory, jsonify
from flask_cors import *  # 导入模块
from passlib.hash import sha256_crypt


import requests
app = Flask(__name__)

pymysql.install_as_MySQLdb()
class Config():
    """配置参数"""
    # 设置连接数据库的URL
    user = 'root'
    password = 'asd007881'
    database = 'laat'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://%s:%s@localhost:3306/%s' % (user,password,database)

    # 设置sqlalchemy自动更跟踪数据库
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # 查询时会显示原始SQL语句
    app.config['SQLALCHEMY_ECHO'] = True

    # 禁止自动提交数据处理
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = False
app.config.from_object(Config)

# 创建数据库sqlalchemy工具对象
db = SQLAlchemy(app)

# class User(db.Model):
#     # 定义表名
#     __tablename__ = 'user'
#     # 定义字段
#     id = db.Column(db.Integer, primary_key=True,autoincrement=True)
#     username = db.Column(db.String(45), unique=False, index=True)
#     password = db.Column(db.String(128),unique=False)
#     user_ch=db.Column(db.String(45),unique=False)


# class User(db.Model):
#     # 定义表名
#     __tablename__ = 'user'
#     # 定义字段
#     """
#     account:账户名
#     password：密码
#     name：名字
#     token：token
#     age：年龄
#     sex：性别
#     avatar：头像
#     type：用户类型
#     permissions：用户权限
#     desc：描述，简介
#     """
#     id = db.Column(db.Integer, primary_key=True,autoincrement=True)
#     account = db.Column(db.String(45), unique=True, index=True)
#     password = db.Column(db.String(128),unique=False)
#     name=db.Column(db.String(45),unique=False)
#     token=db.Column(db.String(45),unique=False)
#     age = db.Column(db.Integer, unique=False)
#     sex = db.Column(db.Integer, unique=False)
#     avatar = db.Column(db.String(45), unique=False)
#     type=db.Column(db.String(45),unique=False)
#     permissions = db.Column(db.String(100), unique=False)
#     desc = db.Column(db.String(45), unique=False)


# class Booking(db.Model):
#     # 定义表名
#     __tablename__ = 'booking'
#     # 定义字段
#     """
#     :param
#     serverName:预约机器名
#     bookingName:预约产品名
#     bookingTime:预约时间
#     ip:预约的ip地址
#     testName:测试标题
#     testType:测试内容
#     booking_user:预约用户
#     booking_state:预约状态
#     """
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     serverName = db.Column(db.String(45), unique=False, index=True)
#     bookingName = db.Column(db.String(45), unique=False)
#     bookingTime = db.Column(db.String(45),unique=True)
#     ip = db.Column(db.String(45), unique=False)
#     testName = db.Column(db.String(45), unique=False)
#     testType = db.Column(db.String(45), unique=False)
#     booking_user = db.Column(db.String(45), unique=False)
#     booking_state = db.Column(db.String(45), unique=False)

def hash_password(password):
    password_hash = sha256_crypt.encrypt(password)
    return password_hash

# class Booking(db.Model):
#     # 定义表名
#     __tablename__ = 'booking'
#     # 定义字段
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     serverName = db.Column(db.String(45), unique=False, index=True)
#     bookingName = db.Column(db.String(45), unique=False)
#     bookingTime = db.Column(db.String(45), unique=True)
#     ip = db.Column(db.String(45), unique=False)
#     testName = db.Column(db.String(45), unique=False)
#     testType = db.Column(db.String(45), unique=False)
#     booking_user = db.Column(db.String(45), unique=False)

class Server(db.Model):
    # 定义表名
    __tablename__ = 'server'
    # 定义字段
    """
    :param
    name:tab名
    ip:服务器ip
    img_url:截图url
    state:状态
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    server = db.Column(db.String(45), unique=False, index=True)
    ip = db.Column(db.String(45), unique=False)
    img_url = db.Column(db.String(45),unique=True)
    state = db.Column(db.String(45),unique=False)

def get_ip():
    """
    查询本机ip地址
    :return: ip
    """
    try:
        ip = requests.get('http://icanhazip.com')
        ip.close()
    except ConnectionResetError as e:
        res = requests.get('https://checkip.amazonaws.com')
        ip = res.text.strip()
        res.close()
    finally:
        return ip.text


def send_ip():
    """
    查询本机ip地址
    :return: ip
    """
    try:
        ip=get_ip()
        print(ip)
    except Exception as e:
        print("CATCH ERROR RETRY",e)

    finally:
        data={"ip":str(ip.split('\n')[0])}
        headers={
            "Content-Type":"application/json;charset:utf8"
        }
        requests.post('http://110.40.182.32:5000/set_ip',headers=headers,data=json.dumps(data))

def update_state(server,state):
    try:
        Server.query.filter(Server.server==server).update({"Server.state":state})
        db.session.commit()
    except:
        return jsonify({'statuscode': 400, 'error_msg': '提交失败'})
    return jsonify({'statuscode': 200, 'msg': '提交成功'})

def update_img():
    ip = get_ip()
    ip = str(ip.split('\n')[0])
    # password=sha256_crypt.encrypt("password")
    # user=User(account="Ryan7",password=password,name="Ryan",token="Ryan7",age=26,sex=2,avatar="assets/img/1.71b75fe9.jpg",type='[Vue]',permissions='/futures',desc='描述，简介')
    try:
        Server.query.filter(Server.server=="LAAT 1").update({"img_url":"http://" + ip + ":5000/1"})
        db.session.commit()
        Server.query.filter(Server.server == "LAAT 2").update({"img_url": "http://" + ip + ":5000/2"})
        db.session.commit()
        Server.query.filter(Server.server == "LAAT 3").update({"img_url": "http://" + ip + ":5000/3"})
        db.session.commit()
        Server.query.filter(Server.server == "LAAT 4").update({"img_url": "http://" + ip + ":5000/4"})
        db.session.commit()
    except:
        return jsonify({'statuscode': 400, 'error_msg': '提交失败'})
    print("finish update")
    return jsonify({'statuscode': 200, 'msg': '提交成功'})

if __name__ == "__main__":
    send_ip()
    update_img()
    old_ip=get_ip()
    while True:
        new_ip=get_ip()
        if new_ip!=old_ip:
            send_ip()
            update_img()
            old_ip=new_ip
        else:
            time.sleep(300)
            continue
    # data_arr=[]
    # for i in range(len(data)):
    #     arr= {}
    #     arr['serverName']=data[i].serverName
    #     arr['bookingName']=data[i].bookingName
    #     arr['bookingTime'] = data[i].bookingTime
    #     arr['ip'] = data[i].ip
    #     arr['testName'] = data[i].testName
    #     arr['testType'] = data[i].testType
    #     arr['booking_user'] = data[i].booking_user
    #     data_arr.append(arr)
    # print(data_arr)
    # res=User.query.filter_by(username='test1').all()
    # if res!=[]:
    #     print("账号已注册")

