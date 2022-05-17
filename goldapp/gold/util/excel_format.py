import pandas as pd
from styleframe import StyleFrame, styler
import re
import os


class excel_format:
    def __init__(self):
        pass

    def transformat_from_styleframe(self, dataframe, save_path, columns):
        '''

        :param dataframe: dataframe数据类型的参数
        :param save_path: 保存的路径
        :param columns: 字段组成的列表
        :return:
        '''

        sf = StyleFrame(dataframe)
        excel_writer = StyleFrame.ExcelWriter(save_path)
        sf.to_excel(
            # columns_and_rows_to_freeze="B2",
            best_fit=columns,
            row_to_add_filters=0,
            excel_writer=excel_writer
        )
        excel_writer.save()
        excel_writer.close()



if __name__ == '__main__':
    data = excel_format()
    data.transformat_from_styleframe(dataframe='', save_path='')
