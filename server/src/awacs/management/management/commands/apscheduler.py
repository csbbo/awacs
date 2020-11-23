import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from django.core.management.base import BaseCommand
from pypinyin import Style, pinyin

from stock.models import Stock

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def update_stocks():
    pro = settings.TU_SHARE_PRO
    fields = 'ts_code,symbol,name,area,industry,fullname,enname,market,exchange,curr_type,list_status,list_date,' \
             'delist_date,is_hs '
    df = pro.query('stock_basic', exchange='', list_status='L', fields=fields)

    def short_pinyin(name):
        s = ''
        for letter in pinyin(name, style=Style.FIRST_LETTER, strict=False):
            s += letter[0][0]
        return s

    for row in df.itertuples():
        row_data = {
            'ts_code': row[1],
            'symbol': row[2],
            'name': row[3],
            'short_pinyin': short_pinyin(row[3]),
            'area': row[4],
            'industry': row[5],
            'fullname': row[6],
            'enname': row[7],
            'market': row[8],
            'exchange': row[9],
            'curr_type': row[10],
            'list_status': row[11],
            'list_date': row[12],
            'delist_date': row[13],
            'is_hs': row[14],
        }
        try:
            stock = Stock.objects.get(symbol=row_data['symbol'])

            has_update = False
            for k, v in row_data.items():
                if getattr(stock, k) != v:
                    setattr(stock, k, v)
                    has_update = True

            if has_update:
                stock.save()
                logger.info("Update a stock")
            else:
                logger.info("Nothing is updated")
        except Stock.DoesNotExist:
            Stock.objects.create(**row_data)
            logger.info("Add new stock")
    logger.info("Update or create stock success!")


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)

        scheduler.add_job(update_stocks, 'cron', day_of_week='mon-fri', hour=9)
        # scheduler.add_job(update_stocks, 'interval', seconds=10)
        logger.info("Added job 'my_job'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
