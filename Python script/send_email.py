# -*- coding: utf-8 -*-
# author: Ryan
# time: 2021/9/28
import smtplib
import email
# 负责构造文本
from email.mime.text import MIMEText
# 负责构造图片
from email.mime.image import MIMEImage
# 负责将多个对象集合起来
from email.mime.multipart import MIMEMultipart
from email.header import Header
def send_email(server,recv_email):
    # SMTP服务器,这里使用163邮箱
    mail_host = "smtp.163.com"
    # 发件人邮箱
    mail_sender = "laat_la@163.com"
    # 邮箱授权码,注意这里不是邮箱密码,如何获取邮箱授权码,请看本文最后教程
    mail_license = "SWEUZVEEOFZBNFLL"
    # 收件人邮箱，可以为多个收件人
    mail_receivers = [str(recv_email)]

    mm = MIMEMultipart('related')

    # 邮件主题
    subject_content = """LAAT 有空闲机器，请及时进行测试"""
    # 设置发送者,注意严格遵守格式,里面邮箱为发件人邮箱
    mm["From"] = "<laat_la@163.com>"
    # 设置接受者,注意严格遵守格式,里面邮箱为接受者邮箱
    mm["To"] = str(recv_email)
    # 设置邮件主题
    mm["Subject"] = Header(subject_content,'utf-8')
    # 邮件正文内容
    body_content = """你好，收到本邮件即代表您预约的自动化测试任务可以进行了，本次空闲的自动化测试机器为"""+server+""",如有特殊情况无法进行测试，请及时联系我，后续有计划时需重新预约"""
    # 构造文本,参数1：正文内容，参数2：文本格式，参数3：编码方式
    message_text = MIMEText(body_content,"plain","utf-8")
    # 向MIMEMultipart对象中添加文本对象
    mm.attach(message_text)

    # 创建SMTP对象
    stp = smtplib.SMTP()
    # 设置发件人邮箱的域名和端口，端口地址为25
    stp.connect(mail_host, 25)
    # set_debuglevel(1)可以打印出和SMTP服务器交互的所有信息
    stp.set_debuglevel(1)
    # 登录邮箱，传递参数1：邮箱地址，参数2：邮箱授权码
    stp.login(mail_sender,mail_license)
    # 发送邮件，传递参数1：发件人邮箱地址，参数2：收件人邮箱地址，参数3：把邮件内容格式改为str
    stp.sendmail(mail_sender, mail_receivers, mm.as_string())
    print("邮件发送成功")
    # 关闭SMTP对象
    stp.quit()
if __name__ == "__main__":
    send_email("LAAT2","wujun12@lenovo.com")