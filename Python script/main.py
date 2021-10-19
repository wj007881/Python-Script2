# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from passlib.hash import sha256_crypt
import requests
from flask import send_file
def print_hi():
    # Use a breakpoint in the code line below to debug your script.
    img = requests.get('http://192.168.50.161')
    f=open("./ss.png","wb+")
    f.write(img.content)
    f.close()
    return send_file('./ss.png', mimetype='image/gif')# Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print(print_hi())

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
