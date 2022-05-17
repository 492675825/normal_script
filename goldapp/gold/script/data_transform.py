import shutil
import time

import pandas as pd
import numpy as np
import re
import os
import logging
from goldapp.gold.script import log_function
import warnings
from tqdm import tqdm
from goldapp.gold.mysql_db.script import insert_date

pd.set_option('display.float_format', lambda x: '%.2f' % x)

warnings.filterwarnings("ignore")

pd.set_option("display.max_columns", 100)
pd.set_option("expand_frame_repr", False)


class data_transform:

    def __init__(self):
        self.input_csv_path = os.path.dirname(os.path.dirname(__file__)) + '/historical_data/'
        self.save_path = os.path.dirname(os.path.dirname(__file__)) + '/output/'
        self.backup_path = os.path.dirname(os.path.dirname(__file__)) + '/error_data/'
        self.spider_path = os.path.dirname(os.path.dirname(__file__)) + '/input/'

        if not os.path.exists(self.input_csv_path):
            os.mkdir(self.input_csv_path)
        if not os.path.exists(self.save_path):
            os.mkdir(self.save_path)

    def delete_data(self):
        # 删除20090101之前的数据
        version_date_list = list(range(20000000, 20090000))
        file_list = os.listdir(self.input_csv_path)
        for fl in file_list:
            ver = fl.replace(".csv", '')
            version_number = ver.split("_")[-1]
            # print(version_number)
            if int(version_number) in version_date_list:
                os.remove(self.input_csv_path + fl)
                # logging.info(f">>> [delete] {fl}..")
        print(">>> [Complete] delete table complete..")

    def move_data(self):
        new_data_info = []
        new_data_list = os.listdir(self.spider_path)
        temp_date_list = [d.split("_")[-1] for d in new_data_list]
        get_date_list = [d.replace(".csv", "") for d in temp_date_list]
        historical_data_list = os.listdir(self.input_csv_path)
        temp_his_data_list = [d.split("_")[-1] for d in historical_data_list]
        his_data_list = [d.replace(".csv", "") for d in temp_his_data_list]
        for date, new_data in zip(get_date_list, new_data_list):
            if date in his_data_list:
                new_data_info.append("find")
            else:
                shutil.copy(self.spider_path + new_data, self.input_csv_path + new_data)
                print(f">>> [Find] new data '{new_data}' was find..")
        if len(new_data_info) == len(new_data_list):
            print(">>> [Not Update] Not new data need to update..")
        else:
            print(">>> [Complete] move new data into historical folder..")

    def merge_data(self):
        file_list = os.listdir(self.input_csv_path)
        row_date_list = [ver.replace(".csv", '') for ver in file_list]
        clean_date_list = [v.split("_")[-1] for v in row_date_list]
        columns_list = ["合约", "开盘价", "最高价", "最低价", "收盘价", "涨跌（元）"]
        sample = ['sample', '0.0', '0.0', '0.0', '0.0', '0.0']
        data = pd.DataFrame([sample], columns=columns_list)
        data['日期'] = '20000101'

        for file_name, date_name in tqdm(zip(row_date_list, clean_date_list)):
            try:
                data_frame = pd.read_csv(self.input_csv_path + f'{file_name}.csv')
                data_filter = data_frame[["合约", "开盘价", "最高价", "最低价", "收盘价", "涨跌（元）"]]
                data_filter['日期'] = date_name
                data = pd.concat([data, data_filter], axis=0)
            except Exception as e:
                shutil.copy(self.input_csv_path + f'{file_name}.csv', self.backup_path + f'{file_name}.csv')

        data = data.dropna(axis=0)
        data.columns = ["item", "open", "high", "low", "close", "up_or_down", "version_date"]

        data.to_excel(self.save_path + f'{time.strftime("%Y%m%d")}.xlsx')
        final_data = pd.read_excel(self.save_path + f'{time.strftime("%Y%m%d")}.xlsx')
        final_data.columns = ["id", "item", "open", "high", "low", "close", "up_or_down", "version_date"]
        for i in range(len(final_data)):
            final_data["id"][i] = i + 1
        print(">>> [Complete] merge table complete.. ")
        return final_data

    def main(self):
        self.delete_data()
        self.move_data()

        # 插入数据库
        df = self.merge_data()
        db = insert_date.MySQLUtil(host='localhost', port='3306', username='root',
                                   password='123456', db='finance_analysis_20211219db',
                                   table='temp_gold_data')
        db.df_write_mysql(df)


if __name__ == '__main__':
    data = data_transform()
    data.main()
    # data.union_csv_file()
