import authlib
import requests
from flask_sqlalchemy import SQLAlchemy

from flask_httpauth import HTTPBasicAuth,HTTPTokenAuth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired

from flask import current_app, g, make_response, jsonify,Flask,request
import socket

db = SQLAlchemy()


auth=HTTPTokenAuth(scheme='JWT')

tokens=[]

app=Flask(__name__)
app.config['SECRET_KEY']="asd007881"

@auth.verify_token
def verify_token(token):
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


@app.route('/get_token',methods=['POST'])
def generate_auth_token(expiration=3600):
    data=request.json
    print(data)
    username=data['username']
    s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
    token=str(s.dumps({'id': username}))
    tokens.append(token)
    return jsonify({"token":token,"username":username})


@app.route('/404')
@auth.login_required
def erroer_404():
    return "404 Not found"

@app.route('/')
@auth.login_required
def index():
    return "hello"

if __name__ == "__main__":
    hostname = socket.gethostname()
    # 获取本机ip
    ip = socket.gethostbyname(hostname)
    # ip=get_host_ip()
    app.debug = True
    app.run(host=ip, port=5000)
