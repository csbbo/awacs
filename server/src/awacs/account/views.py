from django.http import JsonResponse
from django.core.cache import cache
import json

from utils.api import APIView


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
