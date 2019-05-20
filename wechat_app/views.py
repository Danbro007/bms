from django.shortcuts import render
import configparser
from wechat.settings import *


def WechatLogin(req):
    if req.method == "GET":
        return render(req, "wechat/wechat_login/login.html")


def wecaht_login():
    config = configparser.ConfigParser()
    config.read(os.path.join(BASE_DIR, "itchat_part", "wechat.cfg"), encoding='utf-8')
    return eval(config.get("status", "login"))
