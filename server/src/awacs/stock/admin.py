from django.contrib import admin
from stock.models import *


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('symbol', 'name', 'industry', 'area', 'market', 'short_pinyin', 'list_date', 'list_status')
    list_display_links = ('symbol', 'name')
    search_fields = list_display
    list_filter = ('industry', 'area', 'market')


@admin.register(SubscribeStock)
class SubscribeStockAdmin(admin.ModelAdmin):
    list_display = ('symbol', 'name', 'refer')


@admin.register(Optional)
class OptionalAdmin(admin.ModelAdmin):
    list_display = ('symbol', 'name')
