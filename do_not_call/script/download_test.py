import requests
import os
import pandas as pd
from lxml.html import etree
import time
import traceback


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
        try:
            print("0-Download Start..")
            session = requests.session()
            login = session.post(url=self.url, data=self.form_data, headers=self.header)
            # 获取cookie，用于之后的使用
            html_login = etree.HTML(login.text)
            login_UserHashSeq = html_login.xpath('//input[@name="UserHashSeq"]/@value')[0]
            print("1-Get UserHashSeq..")
            print('login_UserHashSeq:', login_UserHashSeq)
            time.sleep(5)
            cookie = login.cookies
            self.form_data_download = {
                "RegisterType": "S",
                "ButtonAction": "download",
                "SourceType": "ContainDate",
                "UserSeq": "3",
                "UserHashSeq": f"{login_UserHashSeq}"
            }
            download_file_res = session.post(url=self.download_url,
                                             data=self.form_data_download,
                                             headers=self.header,
                                             cookies=cookie)
            html = etree.HTML(download_file_res.text)
            md5_code = html.xpath('//input[@name="CheckSum"]/@value')[0]
            SHA256_code = html.xpath('//input[@name="CheckSumSHA256"]/@value')[0]
            ListFileName = html.xpath('//input[@name="ListFileName"]/@value')[0]
            ChecksumFileNameMD5 = html.xpath('//input[@name="ChecksumFileNameMD5"]/@value')[0]
            ChecksumFileNameSHA256 = html.xpath('//input[@name="ChecksumFileNameSHA256"]/@value')[0]
            SubFolder = html.xpath('//input[@name="SubFolder"]/@value')[0]
            ListFileDownloadName = html.xpath('//input[@name="ListFileDownloadName"]/@value')[0]
            ChecksumDownloadNameMD5 = html.xpath('//input[@name="ChecksumDownloadNameMD5"]/@value')[0]
            ChecksumDownloadNameSHA256 = html.xpath('//input[@name="ChecksumDownloadNameSHA256"]/@value')[0]
            SourceFileName = html.xpath('//input[@name="SourceFileName"]/@value')[0]
            SourceSize = html.xpath('//input[@name="SourceSize"]/@value')[0]
            SourceChecksumMD5 = html.xpath('//input[@name="SourceChecksumMD5"]/@value')[0]
            SourceChecksumSHA256 = html.xpath('//input[@name="SourceChecksumSHA256"]/@value')[0]
            SourceFileDate = html.xpath('//input[@name="SourceFileDate"]/@value')[0]
            SortedChecksumMD5 = html.xpath('//input[@name="SortedChecksumMD5"]/@value')[0]
            SortedChecksumSHA256 = html.xpath('//input[@name="SortedChecksumSHA256"]/@value')[0]
            UserSeq = html.xpath('//input[@name="UserSeq"]/@value')[0]
            UserHashSeq = html.xpath('//input[@name="UserHashSeq"]/@value')[0]
            self.download_url_md5 = f'https://www.dnc.gov.hk/download/{ListFileName}'
            print("md5_url:", self.download_url_md5)
            self.form_data_md5 = {
                "RegisterType": "S"
                , "CheckSum": f"{md5_code}"
                , "CheckSumSHA256": f"{SHA256_code}"
                , "DownloadChecksumMD5": f"Download MD5"
                , "DownloadType": "DownloadChecksumMD5"
                , "ListFileName": f"{ListFileName}"
                , "ChecksumFileNameMD5": f"{ChecksumFileNameMD5}"
                , "ChecksumFileNameSHA256": f"{ChecksumFileNameSHA256}"
                , "SubFolder": f"{SubFolder}"
                , "ListFileDownloadName": f"{ListFileDownloadName}"
                , "ChecksumDownloadNameMD5": f"{ChecksumDownloadNameMD5}"
                , "ChecksumDownloadNameSHA256": f"{ChecksumDownloadNameSHA256}"
                , "SourceFileName": f"{SourceFileName}"
                , "SourceSize": f"{SourceSize}"
                , "SourceChecksumMD5": f"{SourceChecksumMD5}"
                , "SourceChecksumSHA256": f"{SourceChecksumSHA256}"
                , "SourceFileDate": f"{SourceFileDate}"
                , "SortedChecksumMD5": f"{SortedChecksumMD5}"
                , "SortedChecksumSHA256": f"{SortedChecksumSHA256}"
                , "UserSeq": f"{UserSeq}"
                , "UserHashSeq": f"{UserHashSeq}"
            }
            print("2-Download MD5 File..")
            print("form_data_md5:", self.form_data_md5)
            time.sleep(5)
            md5_file_res = session.post(url=self.download_url_md5,
                                        data=self.form_data_md5,
                                        headers=self.header,
                                        cookies=cookie)
            with open(F"{ChecksumFileNameMD5}", 'wb') as md5_f:
                md5_f.write(md5_file_res.content)
            print("Running Complete..")
        except Exception as e:
            print("Login failed..")
            print(traceback.print_exc())

    def test(self):
        html_file_name = 'download_html.html'
        res = open(html_file_name, 'r', encoding='utf-8').read()
        html = etree.HTML(res)
        md5_code = html.xpath('//input[@name="CheckSum"]/@value')[0]
        print(md5_code)
        SHA256_code = html.xpath('//input[@name="CheckSumSHA256"]/@value')[0]
        print(SHA256_code)
        ListFileName = html.xpath('//input[@name="ListFileName"]/@value')[0]
        print(ListFileName)
        ChecksumFileNameMD5 = html.xpath('//input[@name="ChecksumFileNameMD5"]/@value')[0]
        print(ChecksumFileNameMD5)
        ChecksumFileNameSHA256 = html.xpath('//input[@name="ChecksumFileNameSHA256"]/@value')[0]
        print(ChecksumFileNameSHA256)
        SubFolder = html.xpath('//input[@name="SubFolder"]/@value')[0]
        print(SubFolder)
        ListFileDownloadName = html.xpath('//input[@name="ListFileDownloadName"]/@value')[0]
        print(ListFileDownloadName)
        ChecksumDownloadNameMD5 = html.xpath('//input[@name="ChecksumDownloadNameMD5"]/@value')[0]
        print(ChecksumDownloadNameMD5)
        ChecksumDownloadNameSHA256 = html.xpath('//input[@name="ChecksumDownloadNameSHA256"]/@value')[0]
        print(ChecksumDownloadNameSHA256)
        SourceFileName = html.xpath('//input[@name="SourceFileName"]/@value')[0]
        print(SourceFileName)
        SourceSize = html.xpath('//input[@name="SourceSize"]/@value')[0]
        print(SourceSize)
        SourceChecksumMD5 = html.xpath('//input[@name="SourceChecksumMD5"]/@value')[0]
        print(SourceChecksumMD5)
        SourceChecksumSHA256 = html.xpath('//input[@name="SourceChecksumSHA256"]/@value')[0]
        print(SourceChecksumSHA256)
        SourceFileDate = html.xpath('//input[@name="SourceFileDate"]/@value')[0]
        print(SourceFileDate)
        SortedChecksumMD5 = html.xpath('//input[@name="SortedChecksumMD5"]/@value')[0]
        print(SortedChecksumMD5)
        SortedChecksumSHA256 = html.xpath('//input[@name="SortedChecksumSHA256"]/@value')[0]
        print(SortedChecksumSHA256)
        UserSeq = html.xpath('//input[@name="UserSeq"]/@value')[0]
        print(UserSeq)
        UserHashSeq = html.xpath('//input[@name="UserHashSeq"]/@value')[0]
        print(UserHashSeq)


if __name__ == '__main__':
    data = download_fun()
    data.download()
