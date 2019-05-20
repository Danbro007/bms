import time
from wxpy import *
import os
import requests
import random
import configparser
import re

os.environ['DJANGO_SETTINGS_MODULE'] = 'wechat.settings'
import django

django.setup()
from wechat_app.models import *
from wechat.settings import STATICFILES_DIRS, BASE_DIR
from bs_system.module.adminManage.models import *
from bs_system.module.role.models import RoleAuth
from bs_system.module.rule.models import Auth

auths = RoleAuth.objects.filter(role__accountrole__account__username="sqj").values("auth__act", "role_id",
                                                                                   "auth__permission_url").distinct()


def init_permission(auths):
    permissions_dict = {}
    for auth in auths:
        if not permissions_dict.get(auth["role_id"]):
            permissions_dict[auth["role_id"]] = {
                "url": [auth["auth__permission_url"]],
                "action": [auth["auth__act"]]
            }
        else:
            permissions_dict[auth["role_id"]]["url"].append(auth["auth__permission_url"])
            permissions_dict[auth["role_id"]]["action"].append(auth["auth__act"])
    return permissions_dict


test_url = "/admin/company/list/"

for item in init_permission(auths).values():
    flag = False
    for url in item["url"]:
        if re.match(url, test_url):
            print("yes")
            flag = True
    if flag == True:
        break
