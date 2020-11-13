import json
import logging
import os

from django.conf import settings
from django.core.cache import cache

from stock.models import Stock
from stock.serializers import StockSerializer, SubscribeStockSerializer
from utils.api import APIView, check
from utils.shortcuts import is_letter, df_to_list, get_today_zero_last

import tushare


logger = logging.getLogger(__name__)


class SearchStockAPI(APIView):
    def get(self, request):
        data = request.data
        search = data.get('s', None)
        if not search:
            return self.error('查询不能为空!')

        if search.isdigit():
            query = {'symbol__startswith': search}
        elif is_letter(search):
            query = {'short_pinyin__startswith': search.lower()}
        else:
            query = {'name__icontains': search}
        stocks = Stock.objects.filter(**query)
        stocks = StockSerializer(stocks, many=True).data

        data = self.paginate_data(stocks, StockSerializer, force=False)
        return self.success(data=data)


class StockPriceAPI(APIView):
    def get(self, request):
        data = request.data
        code = data.get('code', None)
        if not code:
            return self.error('查询不能为空')
        try:
            df = tushare.get_realtime_quotes(code)
            price = float(df.at[0, 'price'])
            pre_close = float(df.at[0, 'pre_close'])
            data = {
                'name': df.at[0, 'name'],
                'code': df.at[0, 'code'],
                'open': df.at[0, 'open'],
                'pre_close': pre_close,
                'price': price,
                'rose': f"{round((price - pre_close) / pre_close * 100, 3)}%",
                'high': df.at[0, 'high'],
                'low': df.at[0, 'low'],
                'date': df.at[0, 'date'],
                'time': df.at[0, 'time'],
            }
        except IndexError:
            return self.error('查询不存在')
        except Exception as e:
            logger.error(e)
            return self.error('查询错误')
        return self.success(data)


class WsAPI(APIView):
    def get(self, request):
        with open(os.path.join(settings.DATA_PATH, 'ws.json'), 'r') as f:
            data = json.load(f)
        code = data.get('code', None)
        data = {}
        try:
            df = tushare.get_realtime_quotes(code)
            for i in range(len(code)):
                price = float(df.at[i, 'price'])
                pre_close = float(df.at[i, 'pre_close'])
                rose = str(round((price - pre_close) / pre_close * 100, 3)) + '%'
                data[i] = rose
        except IndexError:
            return self.error('查询不存在')
        except Exception as e:
            logger.error(e)
            return self.error('查询错误')
        return self.success(data)


class GetNewsAPI(APIView):
    def get(self, request):
        data = request.data
        news_type = data.get('news_type', None)
        if not news_type or news_type not in ['sina', 'wallstreetcn', '10jqka', 'eastmoney', 'yuncaijing']:
            news_type = 'sina'

        news = cache.get(news_type + '_news')
        if not news:
            pro = settings.TU_SHARE_PRO
            zero_time, last_time = get_today_zero_last()
            news = pro.news(src=news_type, start_date=str(zero_time), end_date=str(last_time))
            news = df_to_list(news)
            cache.set(news_type + '_news', news, timeout=60)
        return self.success(news[0])


class WinnerListAPI(APIView):
    def get(self, request):
        pro = settings.TU_SHARE_PRO
        df = pro.top_inst(trade_date='20201112')
        winner_list = df_to_list(df)
        return self.success(winner_list)


class SubscribeAPI(APIView):
    @check(serializer=SubscribeStockSerializer)
    def post(self, request):
        data = request.data
        print(data)
        return self.success()

