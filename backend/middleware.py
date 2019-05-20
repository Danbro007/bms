from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from wechat.settings import NOT_VALID_URL
import re


class ValidPermissionMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path in NOT_VALID_URL:
            return None
        if request.user.is_superuser:
            return None
        if not request.user.is_authenticated:
            return redirect("/login/")
        permissions = request.session.get("permissions")
        print(request.path)
        for item in permissions.values():
            for reg in item["url"]:
                reg = "^%s$" % reg
                if re.match(reg,request.path):
                    print("yes")

        # url = request.path
        # if url not in ["/login/"]:
        #     return None
        # if not request.user.is_authenticated:
        #     return redirect("/login/")
        # else:
        #     permissions = request.session.get("permissions")
        #     print("______",permissions)
