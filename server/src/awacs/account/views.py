import asyncio
import logging

from django.http import JsonResponse
from django.core.cache import cache
import json

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
        stocks = data['stocks']
        msg_template = data['msg_template']
        email = data['email']
        
        data = {
            'err': None,
            'data': None
        }
        return JsonResponse(data)


async def ws_socket(socket):
    logger.error(socket.query_params)
    await socket.accept()
    await socket.send_text('hello')
    await asyncio.sleep(3)
    await socket.send_text('hello1')
    await asyncio.sleep(10)
    await socket.send_text('hello2')
    await asyncio.sleep(3)
    await socket.send_text('hello3')
    await asyncio.sleep(3)
    await socket.send_text('hello4')
    await socket.close()


async def connection_socket(socket):
    await socket.accept()
    await socket.send_text('hello')
    await asyncio.sleep(3)
    await socket.send_text('hello1')
    await asyncio.sleep(10)
    await socket.send_text('hello2')
    await asyncio.sleep(3)
    await socket.send_text('hello3')
    await asyncio.sleep(3)
    await socket.send_text('hello4')
    await socket.close()

