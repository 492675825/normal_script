import pandas as pd
import os
from lxml.html import etree
import requests


# https://www.cnblogs.com/

class blog:
    def __init__(self):
        # url = 'https://www.cnblogs.com/'
        self.url = 'http://www.gebiqu.com/login.php?do=submit'
        self.my_bookcase = 'http://www.gebiqu.com/modules/article/bookcase.php'
        self.accout = '13560313059'
        self.password = 'xy492675825!!'
        self.header = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36"
        }
        self.form_data = {
            "LoginForm[username]": "HughXiong",
            "LoginForm[password]": "xy492675825!!",
            "usecookie": "0",
            "action": "login",
            "submit": "登  录"
        }

    def get_spyder(self):
        res = requests.get(url=self.my_bookcase, headers=self.header)
        res.encoding = res.apparent_encoding
        response = res.text
        print(response)

    def post_spyder(self):
        session = requests.session()
        login = session.post(url=self.url, data=self.form_data, headers=self.header)
        cookie = login.cookies
        my_bookcase = session.get(url=self.my_bookcase, headers=self.header, cookies=cookie)
        res = my_bookcase.text
        print(res)


if __name__ == '__main__':
    data = blog()
    data.post_spyder()