from rest_framework import serializers

from stock.models import Stock


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ('name', 'symbol', 'ts_code')


class SubscribeStockSerializer(serializers.Serializer):
    symbol = serializers.CharField(max_length=16)
    refer = serializers.FloatField(required=False)

    remind_way = serializers.CharField(required=False)
    template = serializers.CharField(required=False)

    rose_percent = serializers.FloatField(required=False)
    drop_percent = serializers.FloatField(required=False)
    warn_price = serializers.FloatField(required=False)
    tech_type = serializers.ListField(child=serializers.CharField())
