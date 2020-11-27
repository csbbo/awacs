import uuid
from django.db import models
from django.contrib.postgres.fields import ArrayField


class Stock(models.Model):
    symbol = models.CharField('股票代码', primary_key=True, max_length=16)
    ts_code = models.CharField('TS代码', max_length=16)
    name = models.CharField('股票名称', max_length=64, db_index=True)
    short_pinyin = models.CharField('简拼', max_length=16, db_index=True)
    area = models.CharField('所在地域', max_length=128)
    industry = models.CharField('所属行业', max_length=128)
    fullname = models.CharField('股票全称', max_length=128)
    enname = models.CharField('英文全称', max_length=256)
    market = models.CharField('市场类型', max_length=16)    # 主板/中小板/创业板/科创板
    exchange = models.CharField('交易所代码', max_length=16)
    curr_type = models.CharField('交易货币', max_length=16)
    list_status = models.CharField('上市状态', max_length=16)   # L上市 D退市 P暂停上市
    list_date = models.CharField('上市日期', max_length=16)
    delist_date = models.CharField('退市日期', max_length=16, null=True)
    is_hs = models.CharField('是否沪深港通标的', max_length=16, null=True)  # N否 H沪股通 S深股通

    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Stock'
        verbose_name_plural = verbose_name


class SubscribeStock(models.Model):
    symbol = models.CharField(primary_key=True, max_length=16)
    name = models.CharField(null=True, max_length=16)
    refer = models.FloatField(null=True)

    remind_way = models.CharField(null=True, max_length=16)
    template = models.CharField(null=True, max_length=16)

    rose_percent = models.FloatField(null=True)
    drop_percent = models.FloatField(null=True)
    warn_price = models.FloatField(null=True)
    tech_type = ArrayField(models.CharField(null=True, blank=True, max_length=128), default=list)

    create_time = models.DateTimeField(auto_now_add=True)
    modify_time = models.DateTimeField(auto_now=True)
    # user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'SubscribeStock'
        verbose_name_plural = verbose_name


class Optional(models.Model):
    symbol = models.CharField(primary_key=True, max_length=16)
    name = models.CharField(null=True, max_length=16)

    create_time = models.DateTimeField(auto_now_add=True)
    modify_time = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Optional'
        verbose_name_plural = verbose_name


class CmdQueryRose(models.Model):
    id = models.IntegerField('ID', primary_key=True)
    symbol = models.CharField('股票代码', max_length=16)
    name = models.CharField('股票名称', null=True, max_length=16)
    short_pinyin = models.CharField('简拼', max_length=16, db_index=True)
    owner = models.CharField('Owner', max_length=16, db_index=True)

    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    modify_time = models.DateTimeField('修改时间', auto_now=True)

    class Meta:
        verbose_name = 'CmdQueryRose'
        verbose_name_plural = verbose_name
