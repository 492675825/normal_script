import requests
import os
import pandas as pd
from lxml.html import etree


# html_file_name = 'download_html.html'
# res = open(html_file_name, 'r', encoding='utf-8').read()
# html = etree.HTML(res)
# md5_code = html.xpath('//input[@name="CheckSum"]/@value')
# print(md5_code)

class download_fun:
    def __init__(self):
        self.url = 'https://www.dnc.gov.hk/tm/login'
        self.download_url = 'https://www.dnc.gov.hk/tm/download'
        self.account = 'haseebp'
        self.pwd = 'Edoo2204#'
        self.form_data = {
            "Login": self.account,
            "Password": self.pwd,
            "SecurityCode": "",
            "UserSeq": "0",
            "UserHashSeq": "null"
        }

        self.header = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36"
        }
        print("form_data:", self.form_data)

    def download(self):
        session = requests.session()
        login = session.post(url=self.url, data=self.form_data, headers=self.header)
        # 获取cookie，用于之后的使用
        cookie = login.cookies
        res = login.text
        print(res)

    def test(self):
        html_file_name = 'download_html.html'
        res = open(html_file_name, 'r', encoding='utf-8').read()
        html = etree.HTML(res)
        md5_code = html.xpath('//input[@name="CheckSum"]/@value')
        print(md5_code)



if __name__ == '__main__':
    data = download_fun()
    data.test()
