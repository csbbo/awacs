import importlib
import inspect
import logging
import re

from django.contrib import admin
from django.contrib.staticfiles.views import serve
from django.urls import path, re_path
from django.conf import settings
from utils.api import APIView
from account import views

logger = logging.getLogger(__name__)


def return_static(request, path, insecure=True, **kwargs):
    return serve(request, path, insecure, **kwargs)


class ExportAPIEntryPoints:
    @classmethod
    def _is_export_api_view(cls, obj):
        return inspect.isclass(obj) and issubclass(obj, APIView) and re.match(r"^.+API$", obj.__name__)

    @classmethod
    def export_urlpatterns(cls):
        _urlpatterns = []
        for item in settings.INSTALLED_APPS:
            try:
                views = importlib.import_module(item + ".views")
            except ModuleNotFoundError:
                continue
            views = inspect.getmembers(views, cls._is_export_api_view)
            for name, _class in views:
                url = f"api/{name}"
                _urlpatterns.append(path(url, _class.as_view(), name=name))
                logger.info(f"Detected {name}, url: {url}")
        return _urlpatterns


class ExportWebSocketEntryPoints:
    @classmethod
    def _is_export_api_view(cls, obj):
        return inspect.isfunction(obj) and re.match(r"^.+_socket$", obj.__name__)

    @classmethod
    def export_urlpatterns(cls):
        _urlpatterns = []
        for item in settings.INSTALLED_APPS:
            try:
                views = importlib.import_module(item + ".views")
            except ModuleNotFoundError:
                continue
            views = inspect.getmembers(views, cls._is_export_api_view)
            for name, _method in views:
                url = f"{name.split('_')[0]}"
                _urlpatterns.append(path(url, _method, name=name))
                logger.info(f"Detected {name}, url: {url}")
        return _urlpatterns


api_urls = ExportAPIEntryPoints.export_urlpatterns()
ws_urls = ExportWebSocketEntryPoints.export_urlpatterns()
admin_urls = [
    path('admin/', admin.site.urls),
    re_path(r'^static/(?P<path>.*)$', return_static, name='static'),
]

urlpatterns = api_urls + ws_urls + admin_urls
