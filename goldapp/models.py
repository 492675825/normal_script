from django.db import models


# Create your models here.

class Gold(models.Model):
    # 上海黄金交易所数据模型
    id = models.BigIntegerField(null=False, blank=False, primary_key=True, verbose_name="id")
    item = models.CharField(max_length=100, null=True, blank=True, verbose_name="类别")
    open = models.CharField(max_length=100, null=True, blank=True, verbose_name="开盘价")
    high = models.CharField(max_length=100, null=True, blank=True, verbose_name="最高价")
    low = models.CharField(max_length=100, null=True, blank=True, verbose_name="最低价")
    close = models.CharField(max_length=100, null=True, blank=True, verbose_name="收盘价")
    up_or_down = models.CharField(max_length=100, null=True, blank=True, verbose_name="涨幅")
    version_date = models.DateField(verbose_name="涨幅")

    class Meta:
        db_table = "temp_gold_data"
        verbose_name = '黄金价格'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.item


# 从数据库取出AU(T+D)的数据
class Historical_Gold_Data(models.Model):
    id = models.BigIntegerField(null=False, blank=False, primary_key=True, verbose_name="id")
    version_date = models.DateField(verbose_name="日期")
    item = models.FloatField(null=True, blank=True, verbose_name="类别")
    open = models.FloatField(null=True, blank=True, verbose_name="开盘价")
    high = models.FloatField(null=True, blank=True, verbose_name="最高价")
    low = models.FloatField(null=True, blank=True, verbose_name="最低价")
    close = models.FloatField(null=True, blank=True, verbose_name="收盘价")
    up_or_down = models.FloatField(null=True, blank=True, verbose_name="涨幅")
    mapping = models.IntegerField(null=True, blank=True, verbose_name="数字映射")
    refresh_date = models.DateField(verbose_name="系统刷新时间")

    class Meta:
        db_table = "tbl_au_td_gold_data_analysis"
        verbose_name = '黄金价格'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.item


# 黄金年平均涨跌频率
class Year_Up_Or_Down(models.Model):
    id = models.BigIntegerField(null=False, blank=False, primary_key=True, verbose_name="id")
    year_number = models.CharField(max_length=20, null=False, blank=False, verbose_name="年")
    frequency = models.IntegerField(null=False, blank=False, verbose_name="频率")

    class Meta:
        db_table = "tbl_y_au_td_gold_data_analysis"
        verbose_name = '黄金价格'
        verbose_name_plural = db_table

    def __str__(self):
        return self.id


# 黄金年平均收盘价
class Year_Close(models.Model):
    id = models.BigIntegerField(null=False, blank=False, primary_key=True, verbose_name="id")
    year_number = models.CharField(max_length=20, null=False, blank=False, verbose_name="年")
    average_price = models.FloatField(null=False, blank=False, verbose_name="频率")

    class Meta:
        db_table = "tbl_y_au_td_average_analysis"
        verbose_name = '黄金价格'
        verbose_name_plural = db_table

    def __str__(self):
        return self.id


# 记事本功能
class Note(models.Model):
    id = models.BigIntegerField(null=False, blank=False, primary_key=True, verbose_name="id")
    version_date = models.DateField(null=True, blank=False, verbose_name="时间")
    context = models.CharField(max_length=1000, blank=True, null=True, verbose_name="内容")

    class Meta:
        db_table = "tbl_au_note"
        verbose_name = '黄金价格'
        verbose_name_plural = db_table

    def __str__(self):
        return self.id

# 非农数据
class NonFarm(models.Model):
    id = models.BigIntegerField(null=False, blank=False, primary_key=True, verbose_name="id")
    version_date = models.DateField(null=True, blank=False, verbose_name="时间")
    current_value = models.CharField(max_length=100, blank=True, null=True, verbose_name="当前值")
    predict_value = models.CharField(max_length=100, blank=True, null=True, verbose_name="预测值")
    previous_value = models.CharField(max_length=100, blank=True, null=True, verbose_name="上期值")
    refresh_date = models.CharField(max_length=100, blank=True, null=True, verbose_name="更新时间")

    class Meta:
        db_table = "tbl_non_farm_data"
        verbose_name = "非农数据"
        verbose_name_plural = db_table

    def __str__(self):
        return self.id

