import os

from django.http import JsonResponse
from django.shortcuts import render
from django.template.context_processors import request
from django.views.generic.base import View
import pandas as pd
import time
from goldapp.gold.script import nonfarm_data
from goldapp.gold.mysql_db.script import insert_date

from goldapp.gold.script import run_app
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from goldapp import models
from django.db import connection
from django.core.paginator import Paginator  # 分页
from django.http import FileResponse  # 文件下载


# 爬虫/插入数据库
@csrf_exempt
def get_data_from_web(request):
    if request.method == 'GET':
        # 删除表中的所有数据
        # truncat_order = models.Gold.objects.filter().delete()
        # 清空表(利用原生方法)
        cursor = connection.cursor()
        cursor.execute('truncate table finance_analysis_20211219db.temp_gold_data;')
        cursor.execute("SET @@global.sql_mode= '';")  # 将数据库调整为非严格模式，防止插入数据库中的数据过多报错
        data = run_app.run()
        data.app_run()
        # refresh_date = time.strftime("%Y%m%d %H%M%S")
        context = {"code": 0, "message": "Yeah, success..."}
        return JsonResponse(context)
    else:
        context = {"code": 400, "message": "Opps, error..."}
        return JsonResponse(context)


# 表格：将数据库中的内容呈现在前端表格
def all_gold_data(request):
    if request.method == 'GET':
        gold_list = models.Historical_Gold_Data.objects.all().order_by("-version_date").values()
        context = {"code": 0, "message": "success", "data": list(gold_list)}
        return JsonResponse(context)
    else:
        context = {"code": 0, "message": "error"}
        return JsonResponse(context)


# 分页展示
@csrf_exempt
def page_gold_data(request):
    if request.method == 'POST':
        current_page = request.GET.get("currentPage", "1")
        page_size = request.GET.get("pageSize", "20")
        # 获取数据库所有数据
        all_gold_data = models.Historical_Gold_Data.objects.all().order_by("-version_date")
        # 实例化分页对象（参数1：数据库对象，参数2：每页显示的数量）
        paginator = Paginator(all_gold_data, page_size)
        # 数据总数
        total_record_count = paginator.count
        # 分页后总页数
        total_page_count = paginator.num_pages
        # 分页的页码列表（可用可不用）
        page_list = paginator.page_range
        # 实例化当前指定页对象
        page_target = paginator.page(current_page)
        # 获取当前页的数据
        output_page_data = page_target.object_list.values()
        # 系统刷新时间
        refresh_date = models.Historical_Gold_Data.objects.values("refresh_date").first()
        # print(refresh_date)
        data = {
            "total_record_count": total_record_count,
            "total_page_count": total_page_count,
            "page_list": list(page_list),
            "output_page_data": list(output_page_data),
            "refresh_date": refresh_date["refresh_date"]
        }

        # context = {"code": 0, "message": "success"}
        context = {"code": 0, "message": "success", "data": data}
        return JsonResponse(context)
    else:
        context = {"code": 400, "message": "error"}
        return JsonResponse(context)


# 从数据库导出黄金信息为excel文件
def export_gold_data(request):
    if request.method == "GET":
        data_list = models.Historical_Gold_Data.objects.all().values()
        # 将数据库中的数据保存为csv
        df = pd.DataFrame(list(data_list))
        save_path = os.path.dirname(__file__) + "/gold/save_export_data/"
        save_name = f'gold_data_{time.strftime("%Y%m%d")}.csv'
        df.to_csv(save_path + save_name, index=False)
        # 浏览器端实现文件下载功能
        file = open(save_path + save_name, 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = f'attachment;filename="{save_name}"'
        return response
    else:
        context = {"code": 400, "message": "error"}
        return JsonResponse(context)


# 黄金年涨幅频率（图表）
def yearly_frequency(request):
    if request.method == 'GET':
        # 降序排列取出
        data = models.Year_Up_Or_Down.objects.all().order_by("-year_number").values()
        year_number = [x['year_number'] for x in list(data)]
        frequency = [x['frequency'] for x in list(data)]
        data = {"year_number": year_number, "frequency": frequency}
        context = {"code": 0, "message": "success", "data": data}
        return JsonResponse(context)
    else:
        context = {"code": 400, "message": "error"}
        return JsonResponse(context)


# 黄金年平均收盘价（图表）
def yearly_average_close_price(request):
    if request.method == 'GET':
        # 降序排列取出
        data = models.Year_Close.objects.all().order_by("-year_number").values()
        year_number = [x['year_number'] for x in list(data)]
        average_price = [x['average_price'] for x in list(data)]
        data = {
            "year_number": year_number,
            "average_price": average_price
        }
        context = {"code": 0, "message": "success", "data": data}
        return JsonResponse(context)
    else:
        context = {"code": 400, "message": "error"}
        return JsonResponse(context)


# 记事本功能表格显示
@csrf_exempt
def note(request):
    if request.method == 'GET':
        db_list = models.Note.objects.all().order_by("-id").values()
        context = {"code": 0, "message": "success", "data": list(db_list)}
        return JsonResponse(context)
    else:
        context = {"code": 0, "message": "error"}
        return JsonResponse(context)


# 记事本内容回显功能
def getInfoById(request, id_name):
    if request.method == 'GET':
        # 判断是要新加记录还是回显记录（id_name=0表示不拿mysql的数据，返回空）
        if id_name != "0":
            query = models.Note.objects.filter(id=id_name).values()
            data = query[0]['context']
            context = {"code": 0, "message": "success", "data": data}
            return JsonResponse(context)
        else:
            context = {"code": 0, "message": "success", "data": ''}
            return JsonResponse(context)
    else:
        context = {"code": 0, "message": "success"}
        return JsonResponse(context)


# 记事本添加功能
@csrf_exempt
def addNote(request):
    if request.method == "POST":
        item = request.GET.get("text")
        models.Note.objects.create(version_date=time.strftime("%Y-%m-%d"), context=item)
        return JsonResponse({"code": 0, "message": "success"})
    else:
        return JsonResponse({"code": 400, "message": "error"})


# 记事本删除功能
@csrf_exempt
def deleteById(request):
    if request.method == 'POST':
        id_number = request.GET.get("id_number")
        models.Note.objects.filter(id=id_number).delete()
        return JsonResponse({"code": 0, "message": "success"})
    else:
        return JsonResponse({"code": 400, "message": "error"})


# 记事本更新
@csrf_exempt
def updateById(request):
    if request.method == "POST":
        id_number = request.GET.get("id_number")
        text = request.GET.get("text")
        models.Note.objects.filter(id=id_number).update(context=text)
        return JsonResponse({"code": 0, "message": "success"})
    else:
        return JsonResponse({"code": 400, "message": "error"})


# 指定日期数据返回
@csrf_exempt
def selectByDate(request):
    if request.method == "POST":
        version_date = request.GET.get("version_date")
        date_record = models.Historical_Gold_Data.objects.filter(version_date=version_date).values()
        context = {"code": 0, "message": "success", "data": list(date_record)}
        return JsonResponse(context)
    else:
        context = {"code": 0, "message": "error"}
        return JsonResponse(context)


# 非农数据爬虫
def get_non_farm(request):
    if request.method == 'GET':

        data = nonfarm_data.get_page()  # 调用非农爬虫脚本
        df = data.get_data(showScreen=False)

        cursor = connection.cursor()
        cursor.execute('truncate table finance_analysis_20211219db.tbl_non_farm_data;')
        cursor.execute("SET @@global.sql_mode= '';")  # 将数据库调整为非严格模式，防止插入数据库中的数据过多报错

        # 调用自己写的dataframe插入mysql的脚本
        db = insert_date.MySQLUtil(host='localhost', port='3306', username='root',
                                   password='123456', db='finance_analysis_20211219db',
                                   table='tbl_non_farm_data')
        db.df_write_mysql(df)

        return JsonResponse({"code": 0, "message": "success"})
    else:
        return JsonResponse({"code": 400, "message": "网络错误.."})


# 展示非农数据
@csrf_exempt
def show_non_farm(request):
    if request.method == 'POST':
        current_page = request.GET.get("currentPage", '1')
        page_size = request.GET.get("pageSize", "20")
        non_farm_list = models.NonFarm.objects.all().order_by("-version_date")
        paginator = Paginator(non_farm_list, page_size)
        total_record_count = paginator.count
        total_page_count = paginator.num_pages
        page_target = paginator.page(current_page)
        output_page_data = page_target.object_list.values()
        refresh_date = models.NonFarm.objects.values("refresh_date").first()
        data = {
            "total_record_count": total_record_count,
            "total_page_count": total_page_count,
            "output_page_data": list(output_page_data),
            "refresh_date": refresh_date["refresh_date"]
        }
        return JsonResponse({"code": 0, "message": "success", "data": data})
    else:
        return JsonResponse({"code": 400, "message": "error"})
