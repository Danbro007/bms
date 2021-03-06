import json
from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from .models import *
from django.db import transaction
from django.db.utils import IntegrityError
from django.contrib import auth
from django.contrib.auth import models


def DepartmentList(req):
    """
    部门列表页面的渲染
    :param req:
    :return:
    """
    return render(req, "admin/department/department-list.html")


def DepartmentAdd(req):
    """
    部门添加
    :param req:
    :return:
    """
    if req.method == "GET":
        departments = Department.objects.filter(mark=1).all()
        return render(req, "admin/department/department-add.html", locals())
    else:
        response = {"code": 200, "msg": "部门添加成功"}
        data = {}
        for k, v in req.POST.items():
            if k != "csrfmiddlewaretoken" and v:
                data[k] = v
        try:
            with transaction.atomic():
                if data.get("parent_id"):
                    parent = Department.objects.get(id=data["parent_id"])
                    data["name"] = "------".join([parent.name.rsplit("-", 1)[0], data["name"]])
                else:
                    data["name"] = "|----" + data["name"]
                if Department.objects.filter(name=data["name"], mark=1):
                    raise IntegrityError
                Department.objects.create(**data)
        except IntegrityError:
            response["code"] = 400
            response["msg"] = "部门名已存在"
        except Exception as e:
            response["code"] = 500
            response["msg"] = "服务器出现未知问题【%s】" % e
    return JsonResponse(response)


def DepartmentData(req):
    """
    :param req:
    :return: 返回渲染部门列表所需的数据
    """
    page = int(req.GET.get("page"))
    limit = int(req.GET.get("limit"))
    keyword = req.GET.get("keyword")
    if keyword:
        departments_all = Department.objects.filter(name__contains=keyword, mark=1).all()
    else:
        departments_all = Department.objects.filter(mark=1).all()
    count = departments_all.count()
    departments = departments_all[(page - 1) * limit:page * limit]
    departments_data = []
    for department in departments:
        department_info = {
            "id": department.id,
            "name": department.name,
            "code": department.code,
            "add_time": department.add_time.strftime('%Y-%m-%d'),
        }
        if department.parent is None:
            department_info["parent"] = ""
        else:
            department_info["parent"] = department.parent.name
        departments_data.append(department_info)
    Department_List = {"data": departments_data, "msg": "", "code": 0, "count": count}
    response_data = json.dumps(Department_List)
    return HttpResponse(response_data, content_type="application/json", )


def DepartmentEdit(req, id):
    """
    部门编辑
    :param req:
    :param id:部门id
    :return:
    """
    if req.method == "GET":
        department_info = Department.objects.get(id=id)
        department_info.name = department_info.name.rsplit("-", 1)[1]
        departments = Department.objects.exclude(id=id).all()
        return render(req, "admin/department/department-edit.html", locals())
    else:
        response = {"code": 200, "msg": "修改成功"}
        data = {}
        for k, v in req.POST.items():
            data[k] = v
        if data.get("parent_id"):
            parent = Department.objects.get(id=data["parent_id"])
            data["name"] = "------".join([parent.name.rsplit("-", 1)[0], data["name"]])
        else:
            data["name"] = "|----" + data["name"]
        try:
            with transaction.atomic():
                if Department.objects.filter(name=data["name"], mark=1):
                    raise IntegrityError
                department_obj = Department.objects.get(id=id)
                department_obj.__dict__.update(**data)
                department_obj.save()
        except IntegrityError:
            response["code"] = 400
            response["msg"] = "部门名已存在"
        except Exception as e:
            response["code"] = 500
            response["msg"] = "服务器出现错误"
    return JsonResponse(response)


def DepartmentDel(req):
    """
    部门删除（单个和多个）
    :param req:
    :return:
    """
    if req.method == "POST":
        response = {"code": 200, "msg": "部门删除成功"}
        department_list = json.loads(req.POST.get("id"))
        if not isinstance(department_list, list):
            department_list = [department_list, ]
        try:
            with transaction.atomic():
                Department.objects.filter(id__in=department_list).update(mark=0)
                Department.objects.filter(parent__id__in=department_list).update(mark=0)
        except Exception:
            response["code"] = 500
            response["msg"] = "服务器出现错误"
        return JsonResponse(response)
