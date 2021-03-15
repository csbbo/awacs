import functools
import json

import typing

from django.http import JsonResponse
from django.views.generic.base import View


class APIError(Exception):
    def __init__(self, msg: str, *, err: str = "error"):
        self.err = err
        self.msg = msg
        super().__init__(err, msg)


class APIView(View):
    def _get_request_data(self):
        if self.request.method != "GET":
            json.loads(self.request.body.decode("utf-8"))
        return self.request.GET

    def response(self, data: typing.Union[list, dict, int, float, str] = None, status: int = 200):
        return JsonResponse(data, status=status)

    def success(self, data: typing.Union[list, dict, int, float, str] = None, status: int = 200):
        return JsonResponse({"err": None, "data": data}, status=status)

    def error(self, msg: str, *, err: str = "error", status: int = 200):
        return JsonResponse({"err": err, "msg": msg}, status=status)

    def paginate_data(self, query_set, object_serializer=None, force=False, context=None):
        need_paginate = self.request.GET.get("count", None)
        if need_paginate is None:
            if force:
                raise APIError("'count' is required")
            if object_serializer:
                return object_serializer(query_set, many=True).data
            else:
                return query_set
        try:
            limit = int(self.request.GET.get("count", "100"))
        except ValueError:
            limit = 100
        if limit < 0:
            limit = 100
        try:
            offset = int(self.request.GET.get("offset", "0"))
        except ValueError:
            offset = 0
        if offset < 0:
            offset = 0
        results = query_set[offset:offset + limit]
        if object_serializer:
            count = query_set.count() if not isinstance(query_set, list) else len(query_set)
            results = object_serializer(results, many=True, context=context).data if context \
                else object_serializer(results, many=True).data
        else:
            count = len(query_set)
        data = {"items": results,
                "total": count}
        return data

    def dispatch(self, request, *args, **kwargs):
        request.data = self._get_request_data()
        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)


class check:
    def __init__(self, permission=None, *, serializer=None, serializer_many=False,
                 login_required=True, license_required=True):
        self.permission = permission
        self.serializer = serializer
        self.serializer_many = serializer_many
        self.login_required = login_required
        self.license_required = license_required

        if (serializer_many and not serializer) or (permission and not login_required):
            raise ValueError("Invalid check condition")

    def _check_permission(self, request):
        if self.permission is None:
            return False

        if self.permission == '__all__':
            return True

        user_type = request.user.user_type

        if user_type in self.permission:
            return True
        else:
            return False

    def _get_current_user(self, request):
        user = request.user
        if user.is_authenticated:
            return user
        return None

    def __call__(self, fn):
        @functools.wraps(fn)
        def _check(*args, **kwargs):
            func_self = args[0]
            request = args[1]

            if self.login_required:
                user = self._get_current_user(request)
                if not user:
                    return func_self.login_required()
                request.user = user

                if not self._check_permission(request):
                    return func_self.permission_denied()
            if self.serializer:
                s = self.serializer(data=request.data, many=self.serializer_many)
                if s.is_valid():
                    request.data = s.data
                    request.serializer = self.serializer
                else:
                    return func_self.invalid_serializer(s)
            return fn(*args, **kwargs)
        return _check
