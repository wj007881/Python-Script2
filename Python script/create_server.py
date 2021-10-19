# -*- coding: utf-8 -*-
# author: Ryan
# time: 2021/9/28
import time

from flask_sqlalchemy import SQLAlchemy
import pymysql
from flask import Flask,send_file,request,send_from_directory
from flask_cors import *  # 导入模块
from passlib.hash import sha256_crypt

from create_user import User
from send_email import send_email
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
    bookingName = db.Column(db.String(45), unique=False)
    bookingTime = db.Column(db.String(45),unique=True)
    ip = db.Column(db.String(45), unique=False)
    testName = db.Column(db.String(45), unique=False)
    testType = db.Column(db.String(45), unique=False)
    booking_user = db.Column(db.String(45), unique=False)
    booking_state = db.Column(db.String(45), unique=False)
class Server(db.Model):
    # 定义表名
    __tablename__ = 'server'
    # 定义字段
    """
    :param
    name:tab名
    ip:服务器ip
    img_url:截图url
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    server = db.Column(db.String(45), unique=False, index=True)
    ip = db.Column(db.String(45), unique=False)
    img_url = db.Column(db.String(45),unique=True)
    state = db.Column(db.String(45),unique=False)
def check_state():
    data = Server.query.filter().all()
    for i in data:
            if i.state == "waiting" and len(Booking.query.filter(Booking.booking_state.isnot(None), Booking.booking_state == 'planning').all())>0:

                        bbk=Booking.query.filter(Booking.booking_state.isnot(None), Booking.booking_state == 'planning').first()
                        user=User.query.filter(User.account == bbk.booking_user).first()
                        Booking.query.filter(Booking.booking_user == bbk.booking_user).update({"booking_state": "running"})
                        db.session.commit()
                        Server.query.filter(Server.server==i.server).update({"state":"waiting"})
                        db.session.commit()
                        time.sleep(1)
                        send_email(str(i.server), str(user.email))
            else:
                print('No plan have to run')

if __name__ == "__main__":
        # check_state()
        #
        db.drop_all()
        db.create_all()
        s1=Server(server="LAAT 1",ip='192.168.50.161',img_url="http://116.24.65.161:5000/1",state="waitting")
        s2 = Server(server="LAAT 2", ip='192.168.50.144', img_url="http://116.24.65.161:5000/2", state="waitting")
        s3 = Server(server="LAAT 3", ip='192.168.50.60', img_url="http://116.24.65.161:5000/3", state="waitting")
        s4 = Server(server="LAAT 4", ip='192.168.50.51', img_url="http://116.24.65.161:5000/4", state="waitting")
        db.session.add(s1)
        db.session.add(s2)
        db.session.add(s3)
        db.session.add(s4)
        db.session.commit()
        # data = Server.query.filter().all()
        # for i in data:
        #     Server.query.filter(Server.ip == "192.168.50.15").update({"server": "LAAT 4"})
        #     Server.query.filter(Server.ip == "192.168.50.60").update({"server": "LAAT 3"})
        #     Server.query.filter(Server.ip == "192.168.50.144").update({"server": "LAAT 2"})
        #     Server.query.filter(Server.ip == "192.168.50.161").update({"server": "LAAT 1"})
        #     db.session.commit()