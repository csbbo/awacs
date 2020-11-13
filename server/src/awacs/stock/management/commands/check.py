import time

from stock.models import SubscribeStock
import tushare


def loop():
    subscribes = SubscribeStock.objects.all()
    for sub in subscribes:
        df = tushare.get_realtime_quotes(sub.code)
        price = float(df.at[0, 'price'])
        pre_close = float(df.at[0, 'pre_close'])

        change_percent = round((price - pre_close) / pre_close, 3)
        if sub.rose_percent and change_percent >= sub.rose_percent:
            pass
        if sub.drop_percent and change_percent <= sub.drop_percent:
            pass
        if sub.warn_price and ((price < pre_close and price >= sub.warn_price) or (price > pre_close and price <= sub.warn_price)):
            pass
