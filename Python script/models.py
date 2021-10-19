# -*- coding: utf-8 -*-
# author: Ryan
# time: 2021/9/10
import time,datetime
from send_email import send_email
daytime=time.time()
print(str(datetime.datetime.today()).split(" ")[0])
print(daytime)
def send_to_email():
    send_email("LAAT2", "wujun12@lenovo.com")

if __name__ == "__main__":
    send_to_email()