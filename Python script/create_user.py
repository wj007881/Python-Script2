# -*- coding: utf-8 -*-
# author: Ryan
# time: 2021/9/27
import json
import time

from flask_sqlalchemy import SQLAlchemy
import pymysql
from flask import Flask,send_file,request,send_from_directory
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


class User(db.Model):
    # 定义表名
    __tablename__ = 'user'
    # 定义字段
    """
    account:账户名
    password：密码
    name：名字
    token：token
    age：年龄
    sex：性别
    avatar：头像
    type：用户类型
    permissions：用户权限
    desc：描述，简介
    """
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    account = db.Column(db.String(45), unique=True, index=True)
    password = db.Column(db.String(128),unique=False)
    name=db.Column(db.String(45),unique=False)
    token=db.Column(db.String(45),unique=False)
    age = db.Column(db.Integer, unique=False)
    sex = db.Column(db.Integer, unique=False)
    avatar = db.Column(db.String(45), unique=False)
    type=db.Column(db.String(45),unique=False)
    permissions = db.Column(db.String(100), unique=False)
    desc = db.Column(db.String(45), unique=False)
    email= db.Column(db.String(45), unique=False)
def hash_password(password):
    password_hash = sha256_crypt.encrypt(password)
    return password_hash
if __name__ == "__main__":

    # password=hash_password("15801541027")
    # admin=User(account="taoxq",password=password,name="Baokun",token='',age='26',sex='1',avatar='assets/img/1.71b75fe9.jpg',type='',permissions='/theme',desc="PAPM",email="taoxq2@lenovo.com")
    # db.session.add(admin)
    # db.session.commit()

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

    User.query.filter(User.account == "taoxq").update({"name":'陶秀琴'})
    db.session.commit()
