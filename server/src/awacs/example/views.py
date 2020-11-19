import asyncio
import json
import logging

from asgiref.sync import sync_to_async
from django.core.cache import cache
from django.http import JsonResponse

from stock.models import Stock
from utils.api import APIView

logger = logging.getLogger(__name__)


class HomeTestAPI(APIView):
    def get(self, request):
        data = {
            'err': None,
            'data': None
        }
        key = cache.get("name")
        if key:
            print(key)
        else:
            cache.set('name', 'xiaoming', timeout=100)
        return JsonResponse(data)

    def post(self, request):
        data = json.loads(request.body.decode("utf-8"))
        data = {
            'err': None,
            'data': data['name']
        }
        return JsonResponse(data)


async def ws_socket(socket):
    await socket.accept()
    await socket.send_text('hello')
    await asyncio.sleep(3)
    @sync_to_async
    def query_stock():
        return Stock.objects.filter(name__icontains="长").first()
    s = await query_stock()
    logger.error(s.name)
    await socket.close()