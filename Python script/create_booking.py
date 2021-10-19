# -*- coding: utf-8 -*-
# author: Ryan
# time: 2021/9/24
import datetime
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


class Booking(db.Model):
    # 定义表名
    __tablename__ = 'booking'
    # 定义字段
    """
    :param
    serverName:预约机器名
    bookingName:预约产品名
    bookingTime:预约时间
    ip:预约的ip地址
    testName:测试标题
    testType:测试内容
    booking_user:预约用户
    booking_state:预约状态
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    serverName = db.Column(db.String(45), unique=False, index=True)
    bookingName = db.Column(db.String(45), unique=True)
    bookingTime = db.Column(db.String(45),unique=False)
    ip = db.Column(db.String(45), unique=False)
    testName = db.Column(db.String(45), unique=True)
    testType = db.Column(db.String(45), unique=True)
    booking_user = db.Column(db.String(45), unique=True)
    booking_state = db.Column(db.String(45), unique=False)
# class Server(db.Model):
#     # 定义表名
#     __tablename__ = 'server'
#     # 定义字段
#     """
#     :param
#     name:tab名
#     ip:服务器ip
#     img_url:截图url
#     """
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     server = db.Column(db.String(45), unique=False, index=True)
#     ip = db.Column(db.String(45), unique=False)
#     img_url = db.Column(db.String(45),unique=True)
#     state = db.Column(db.String(45),unique=True)
if __name__ == "__main__":
    # today=str(datetime.datetime.today()).split(" ")[0]
    # booking_list=Booking.query.filter().all()
    # for i in booking_list:
    #     if str(i.bookingTime)[:-9]>today:
    #         print(i.bookingTime)
    # Server.query.filter(Server.server == "LAAT 1").update({"state": "waiting"})
    # sss="admin5"
    # Booking.query.filter(Booking.booking_user==sss).update({"booking_state":"planning"})
    # db.session.commit()
    db.drop_all()
    db.create_all()
