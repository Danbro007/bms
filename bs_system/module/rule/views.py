import json
from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from .models import *
from django.db import transaction
from django.db.utils import IntegrityError
from .tests import module_dict


# 权限
def RuleList(req):
    if req.method == "GET":
        return render(req, "admin/rule/rule-list.html", locals())


def RuleAdd(req):
    if req.method == "GET":
        auths_info = Auth
        auths = Auth.objects.all()
        module = module_dict
        return render(req, "admin/rule/rule-add.html", locals())
    else:
        response = {"code": 200, "msg": "权限添加成功"}
        data = {}
        for k, v in req.POST.items():
            if k != "csrfmiddlewaretoken" and v:
                data[k] = v
        if not data.get("parent_id"):
            data["level"] = 0
            if data.get("act"):
                response["code"] = 401
                response["msg"] = "顶级分类不能设立方法"
                return JsonResponse(response)
        else:
            data["level"] = 1
            if not data.get("act"):
                response["code"] = 403
                response["msg"] = "请选择方法"
                return JsonResponse(response)
            if data["app"] != Auth.objects.get(id=data["parent_id"]).app:
                response["code"] = 402
                response["msg"] = "您选择的父类没有此模块"
                return JsonResponse(response)
        try:
            with transaction.atomic():
                module, app = data["app"].split("/")
                act = data.get("act")
                if not act:
                    act = ""
                data["permission_url"] = get_permissions(module, app, act)
                if Auth.objects.filter(title=data["title"]):
                    raise IntegrityError
                Auth.objects.create(**data)
        except IntegrityError:
            response["code"] = 400
            response["msg"] = "已存在此权限名"
        except Exception as e:
            response["code"] = 500
            response["msg"] = "服务器出现未知问题【%s】" % e
        return JsonResponse(response)


def RuleData(req):
    page = int(req.GET.get("page"))
    limit = int(req.GET.get("limit"))
    keyword_dict = {}
    for k, v in req.GET.items():
        if k != "page" and k != "limit":
            keyword_dict[k] = v
    map_dict = {"rule": "title__contains", "parent": "parent__title__contains", "app": "app__contains",
                "act": "act_contains"}
    search_dict = {}
    for k, v in map_dict.items():
        if keyword_dict.get(k):
            search_dict[v] = keyword_dict[k]
    auths_all = Auth.objects.filter(**search_dict).all()
    auths = auths_all[(page - 1) * limit:page * limit]
    count = auths_all.count()
    auth_data = []
    for auth in auths:
        auth_info = {
            "id": auth.id,
            "title": auth.title,
            "app": auth.app,
            "is_public": auth.is_public,
            "is_menu": auth.is_menu,
            "level": auth.level_name[int(auth.level)][1],
            "act": auth.act
        }
        if auth.parent is None:
            auth_info["parent"] = ""
        else:
            auth_info["parent"] = auth.parent.title
        auth_data.append(auth_info)
    auth_list = {"data": auth_data, "msg": "", "code": 0, "count": count}
    rdata = json.dumps(auth_list)
    return HttpResponse(rdata, content_type="application/json", )


def RuleDel(req):
    if req.method == "POST":
        response = {"code": 200, "msg": "权限删除成功"}
        auth_list = json.loads(req.POST.get("id"))
        if not isinstance(auth_list, list):
            auth_list = [auth_list, ]
        try:
            with transaction.atomic():
                Auth.objects.filter(id__in=auth_list).delete()
        except Exception as e:
            response["code"] = 500
            response["msg"] = "服务器出现未知问题【%s】" % e
        return JsonResponse(response)


def RuleEdit(req, id):
    if req.method == "GET":
        rule = Auth.objects.get(id=id)
        auths = Auth.objects.all()
        auth = Auth
        return render(req, "admin/rule/rule-edit.html", locals())
    else:
        response = {"code": 200, "msg": "权限编辑成功"}
        data = {}
        for k, v in req.POST.items():
            if k != "csrfmiddlewaretoken" and v:
                data[k] = v
        if not data.get("parent_id"):
            data["level"] = 0
            if data.get("act"):
                response["code"] = 401
                response["msg"] = "顶级分类不能设立方法"
                return JsonResponse(response)
        else:
            data["level"] = 1
            if not data.get("act"):
                response["code"] = 403
                response["msg"] = "请选择方法"
                return JsonResponse(response)
            if data["app"] != Auth.objects.get(id=data["parent_id"]).app:
                response["code"] = 402
                response["msg"] = "您选择的父类没有此模块"
                return JsonResponse(response)
        try:
            with transaction.atomic():
                if Auth.objects.filter(title=data["title"]).exclude(id=id):
                    raise IntegrityError
                module, app = data["app"].split("/")
                act = data.get("act")
                if not act:
                    act = ""
                data["permission_url"] = get_permissions(module, app, act)
                rule_obj = Auth.objects.get(id=id)
                rule_obj.__dict__.update(**data)
                rule_obj.save()
        except IntegrityError:
            response["code"] = 400
            response["msg"] = "已存在此权限名"
        except Exception as e:
            response["code"] = 500
            response["msg"] = "服务器出现未知问题【%s】" % e
        return JsonResponse(response)


def get_permissions(module, app, act):
    if act == "edit":
        return "/".join(["/" + module, app, act, "(?P<id>\d+)/"])
    else:
        return "/".join(["/" + module, app, act + "/"])
