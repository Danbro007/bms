from django.shortcuts import render, redirect
from django.contrib import auth
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from wechat_app.models import *
import configparser
from wechat.settings import *
from bs_system.module.adminManage.models import *
from bs_system.module.role.models import RoleAuth
from .init_func import init_permission

# Create your views here.
def Index(req):
    req.session["wechat_login"] = wecaht_login()
    chatrooms = Chatroom.objects.all()
    return render(req, "backend/index.html", locals())


def Welcome(req):
    return render(req, "backend/welcome.html")


def Login(req):
    if req.method == "GET":
        return render(req, "backend/login.html")
    else:
        response = {"code": 200, "msg": ""}
        username = req.POST.get("username")
        password = req.POST.get("password")
        user = auth.authenticate(req, username=username, password=password)
        if user:
            auth.login(req, user)
            auths = RoleAuth.objects.filter(role__accountrole__account__username="sqj").values("auth__act", "role_id",
                                                                                               "auth__permission_url").distinct()
            req.session["permissions"] = init_permission(auths)
        else:
            response["code"] = 400
            response["msg"] = "账号或者密码错误"
        return JsonResponse(response)


def LogOut(req):
    auth.logout(req)
    return redirect("/login/")


def wecaht_login():
    config = configparser.ConfigParser()
    config.read(os.path.join(BASE_DIR, "itchat_part", "wechat.cfg"), encoding='utf-8')
    return eval(config.get("status", "login"))
