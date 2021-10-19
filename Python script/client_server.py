# -*- coding:utf-8 -*-
"""
@software: PyCharm
@file: client_server.py
@time: 2021/8/18 9:52
@author: Ryan
"""
import datetime
import json
import sys,os
import time
from itsdangerous import SignatureExpired,BadSignature
from  itsdangerous   import TimedJSONWebSignatureSerializer as   Serializer
import requests
from flask import Flask, send_file, request, send_from_directory, jsonify
import pyautogui
import socket
import psutil
from flask_sqlalchemy import SQLAlchemy
import pymysql
from flask import Flask,send_file,request,send_from_directory,g
from flask_cors import *  # 导入模块
from passlib.hash import sha256_crypt
from flask_httpauth import HTTPTokenAuth
from send_email import send_email

auth = HTTPTokenAuth(scheme='JWT')
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}},supports_credentials=True)  # 设置跨域

tokens=[]
w = os.path.dirname(os.path.realpath(sys.executable))
w2 = os.path.join(w, "screenshot.png")
pymysql.install_as_MySQLdb()

# 创建数据库sqlalchemy工具对象

class Config():
    """配置参数"""
    # 设置连接数据库的URL
    user = 'root'
    password = 'asd007881'
    database = 'laat'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://%s:%s@localhost:3306/%s' % (user,password,database)
    app.config['SECRET_KEY'] = "asd007881"
    # 设置sqlalchemy自动更跟踪数据库
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # 查询时会显示原始SQL语句
    #app.config['SQLALCHEMY_ECHO'] = True
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # 禁止自动提交数据处理
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = False
app.config.from_object(Config)
db = SQLAlchemy(app)
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
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    account = db.Column(db.String(45), unique=True, index=True)
    password = db.Column(db.String(128), unique=False)
    name = db.Column(db.String(45), unique=False)
    token = db.Column(db.String(45), unique=False)
    age = db.Column(db.Integer, unique=False)
    sex = db.Column(db.Integer, unique=False)
    avatar = db.Column(db.String(45), unique=False)
    type = db.Column(db.String(45), unique=False)
    permissions = db.Column(db.String(100), unique=False)
    desc = db.Column(db.String(45), unique=False)
    email = db.Column(db.String(45), unique=False)


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
    bookingTime = db.Column(db.String(45), unique=False)
    ip = db.Column(db.String(45), unique=False)
    testName = db.Column(db.String(45), unique=True)
    testType = db.Column(db.String(45), unique=True)
    booking_user = db.Column(db.String(45), unique=True)
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

@app.route('/update_state',methods=['POST'])
def update_state():
    req = request.json
    server = str(req['server'])
    state = str(req['state'])
    try:
        Server.query.filter(Server.server==server).update({"state":state})
        db.session.commit()
    except:
        return jsonify({'statuscode': 400, 'error_msg': '提交失败'})
    return jsonify({'statuscode': 200, 'msg': '提交成功'})

@app.route('/update_booking_content',methods=['POST'])
def update_booking_content():
    req = request.json
    id = str(req['id'])
    BookingTime = str(req['bookingTime'])
    Servername = str(req['serverName'])
    booking_state= str(req["bookingState"])
    try:
        Booking.query.filter(Booking.id==id).update({"bookingTime":BookingTime,"serverName":Servername,"booking_state":booking_state})
        db.session.commit()
    except:
        return jsonify({'statuscode': 400, 'error_msg': '提交失败'})
    return jsonify({'statuscode': 200, 'msg': '提交成功'})



@app.route('/get_server_state')
def get_state():
    try:
        data = Server.query.filter().all()
    except:
        return jsonify({'statuscode': 400, 'error_msg': '查询失败'})

    data_arr = []
    for i in range(len(data)):
        res = {}
        res['server'] = data[i].server
        res['state'] = data[i].state
        data_arr.append(res)
    return jsonify(data_arr)


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

def update_img():
    ip = get_ip()
    ip = str(ip.split('\n')[0])
    # password=sha256_crypt.encrypt("password")
    # user=User(account="Ryan7",password=password,name="Ryan",token="Ryan7",age=26,sex=2,avatar="assets/img/1.71b75fe9.jpg",type='[Vue]',permissions='/futures',desc='描述，简介')
    try:
        Server.query.filter(Server.server == "LAAT 1").update({"img_url":"http://" + ip + ":5000/1"})
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






def hash_password(password):
    password_hash = sha256_crypt.encrypt(password)
    return password_hash
def verify_password(password,password_hash):
    verify = sha256_crypt.verify(password,password_hash)
    return verify
def get_host_ip():
    """
    查询本机ip地址
    :return: ip
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

def screenshot():
    img = pyautogui.screenshot()  # x,y,w,h
    img.save(w2)

@app.route('/img')
def send_img():
    screenshot()
    return send_file(w2, mimetype='image/gif')


@auth.verify_token
def get_token(token):
    s = Serializer(app.config['SECRET_KEY'])
    try:
        s.loads(token)
    except BadSignature:
        # AuthFailed 自定义的异常类型
        raise Exception
    except SignatureExpired:
        raise Exception
        # 校验通过返回True
    return True

@app.route('/404')
# @auth.login_required
def error_404():
    return "404 Not found"

@app.route('/index')
# @auth.login_required
def index():
    return "hello"


@app.route('/get_userinfo',methods=['POST'])
def get_userinfo():
    # data=request.get_json()
    # print(data)
    #
    # uname=data['username']
    # pwd=data['password']
    # app.config['SECRET_KEY']='123456'
    print(request.headers.get('Authorization'))
    req = request.json
    account = req['account']
    try:
         data=User.query.filter(User.account == account).first()
    except:
        return jsonify({'statuscode': 400, 'msg': '查询失败，用户名不存在'})
    res={}
    res['account']=data.account
    res['name']=data.name
    res['token']=request.headers.get('Authorization')
    res['age']=data.age
    res['sex']=data.sex
    res['avatar']=data.avatar
    res['type']=data.type
    res['permissions']=data.permissions
    res['desc']=data.desc
    return jsonify(res)


@app.route('/login',methods=['POST'])
def login(expiration=3600):
    # data=request.get_json()
    # print(data)
    #
    # uname=data['username']
    # pwd=data['password']
    # app.config['SECRET_KEY']='123456'
    data = request.json
    account = data['account']
    password = data['password']
    try:
         exits=User.query.filter(User.account == account).first()
    except:
        return jsonify({'statuscode': 400, 'msg': '登陆失败，用户名不存在'})

    s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
    if exits:
        if verify_password(password,exits.password):
            token = s.dumps({'id': account}).decode()
            tokens.append(token)
            return jsonify({'statuscode':200,'msg':'登录成功','token':token})
        else:
            return jsonify({'statuscode': 400, 'msg': '登陆失败，密码错误'})
    else:
        return jsonify({'statuscode':400,'error_msg':'登录失败，请检查用户名密码'})
    return True

@app.route('/register')
def register():
    data=request.get_json()
    uname=data['username']
    pwd=data['password']
    ch_name=data['user_ch']
    if uname is None or pwd is None:
        return jsonify({'statuscode':401,'error_msg':'注册失败，用户名或密码为空'})  # missing arguments
    if User.query.filter_by(username=uname).first() is not None:
        return jsonify({'statuscode':402,'error_msg':'注册失败，用户名已注册'})  # existing user
    user=User(username=uname,user_ch=ch_name)
    user.hash_password(pwd)
    db.session.add(user)
    try:
        db.session.commit()
    except:
       return jsonify({'statuscode':403,'error_msg':'注册失败，再次尝试失败后请联系管理员'})
    return jsonify({'statuscode':200,'msg':'注册成功'})

@app.route('/check_username',methods=['POST'])
def check_username():
    data=request.json
    uname=data['username']
    if User.query.filter(User.username == uname).first():
        return jsonify({'statuscode':200,'error_msg':'用户存在'})
    else:
        return jsonify({'statuscode':400,'error_msg':'用户不存在'})
    return jsonify({'statuscode':400,'error_msg':'查询失败'})

@app.route('/update_booking',methods=['POST'])
# @auth.login_required
def update_booking():
    data=request.json
    print(data)
    id = str(data['id'])
    action = str(data['action'])
    try:
       Booking.query.filter(Booking.id==id).update({'booking_state':action})
       db.session.commit()
    except:
       return jsonify({'statuscode':400,'error_msg':'提交失败'})
    return jsonify({'statuscode':200,'msg':'提交成功'})

@app.route('/booking',methods=['POST'])
# @auth.login_required
def booking():
    data=request.json
    print(data)
    try:
        bookingName = str(data['bookingName'])
        ip = str(request.remote_addr)
        testName = str(data['testName'])
        testType = str(data['testType'])
        booking_user = str(data['booking_user'])
        booking_state = str(data['booking_state'])
        booking1 = Booking(bookingName=bookingName, ip=ip, testName=testName, testType=testType,
                           booking_user=booking_user, booking_state=booking_state)
        db.session.add(booking1)
        db.session.commit()
    except:
       return jsonify({'statuscode':400,'error_msg':'提交失败'})
    return jsonify({'statuscode':200,'msg':'提交成功'})


@app.route('/get_booking')
def get_booking():
    today = str(datetime.datetime.today()).split(" ")[0]
    data = Booking.query.filter(Booking.booking_state.isnot(None),Booking.booking_state!='drop',Booking.booking_state!='finish').all()
    data_arr=[]
    for i in range(len(data)):
        # if str(data[i].bookingTime)[:-9] > today:
            arr = {}
            arr['id'] = data[i].id
            arr['serverName'] = data[i].serverName
            arr['bookingName'] = data[i].bookingName
            arr['bookingTime'] = str(data[i].bookingTime)[:-3]
            arr['ip'] = data[i].ip
            arr['testName'] = data[i].testName
            arr['testType'] = data[i].testType
            arr['booking_user'] = data[i].booking_user
            arr['booking_state'] = data[i].booking_state
            data_arr.append(arr)
    return jsonify(data_arr)

@app.route('/1')
def send_img1():
    img = requests.get('http://192.168.50.161')
    f = open("./s1.png", "wb+")
    f.write(img.content)
    f.close()
    return send_file('./s1.png', mimetype='image/gif')


@app.route('/3')
def send_img2():
    img = requests.get('http://192.168.50.60')
    f = open("./s2.png", "wb+")
    f.write(img.content)
    f.close()
    return send_file('./s2.png', mimetype='image/gif')

@app.route('/2')
def send_img3():
    img=requests.get('http://192.168.50.144')
    f = open("./s3.png", "wb+")
    f.write(img.content)
    f.close()
    return send_file('./s3.png', mimetype='image/gif')


@app.route('/get_img_arr')
def send_img_arr():
    """
    :param
    name:tab名
    ip:服务器ip
    img:截图url
    :return: arr三个服务器的数据集合
    """
    data = Server.query.filter().all()
    data_arr = []
    for i in range(len(data)):
        arr = {}
        arr['id'] = data[i].id
        arr['server'] = data[i].server
        arr['img_url'] = data[i].img_url
        arr['ip'] = data[i].ip
        data_arr.append(arr)
    return jsonify(data_arr)

def get_host_ip():
    """
    查询本机ip地址
    :return: ip
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
        return ip

@app.route("/send_email",methods=['POST'])
def send_to_email():
    data = request.json
    username=data['user']
    user = User.query.filter(User.account==username).first()
    email = user.email
    try:
        machine=data['machine']
    except:
        machine='<待定>'
    try:
        send_email(machine, email)
    except:
        return jsonify({'statuscode': 400, 'error_msg': '发送失败'})
    return jsonify({'statuscode': 200, 'msg': '发送成功'})

if __name__ == "__main__":
    # 获取本机ip
    ip =get_host_ip()
    # ip=get_host_ip()
    app.debug = True
    app.run(host=ip,port=5000)


