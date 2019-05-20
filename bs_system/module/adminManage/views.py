import json
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from bs_system.module.role.models import Role
from bs_system.module.position.models import Position
from bs_system.module.company.models import Company
from bs_system.module.department.models import Department
from django.db import transaction
from .models import Account, AccountRole
from django.db.utils import IntegrityError


def AdminList(req):
    return render(req, "admin/admin/admin-list.html")


def AdminAdd(req):
    if req.method == "GET":
        roles = Role.objects.filter(mark=1)
        positions = Position.objects.filter(mark=1)
        departments = Department.objects.filter(mark=1)
        companies = Company.objects.filter(mark=1)
        return render(req, "admin/admin/admin-add.html", locals())
    else:
        response = {"code": 200, "msg": "用户添加成功"}
        data = {}
        id_list = []
        for k, v in req.POST.items():
            if k != "csrfmiddlewaretoken" and not k.startswith("id"):
                if v:
                    data[k] = v
            if k.startswith("id"):
                id_list.append(v)
        try:
            with transaction.atomic():
                account_obj = Account.objects.create_user(**data)
                for item in id_list:
                    AccountRole.objects.create(role_id=item, account=account_obj)
        except IntegrityError:
            response["code"] = 400
            response["msg"] = "用户名已存在"
        except Exception as e:
            response["code"] = 500
            response["msg"] = "服务器出现错误"
        return JsonResponse(response)


def AdminData(req):
    page = int(req.GET.get("page"))
    limit = int(req.GET.get("limit"))
    search_list = {}
    for k, v in req.GET.items():
        if k != "limit" and k != "page":
            search_list[k] = v
    if any(search_list):
        search_dict = {}
        if search_list["username"]:
            search_dict["username__contains"] = search_list["username"]
        if search_list["company"]:
            search_dict["company__name__contains"] = search_list["company"]
        if search_list["department"]:
            search_dict["department__name__contains"] = search_list["department"]
        if search_list["position"]:
            search_dict["position__name__contains"] = search_list["position"]
        if search_list["role"]:
            search_dict["accountrole__role__name__contains"] = search_list["role"]
        accounts = Account.objects.filter(**search_dict).all()[(page - 1) * limit:page * limit]
        count = Account.objects.filter(**search_dict).all().count()
    else:
        count = Account.objects.filter(mark=1).count()
        accounts = Account.objects.filter(mark=1)[(page - 1) * limit:page * limit]
    roles_data = []
    for account in accounts:
        roles = AccountRole.objects.filter(account=account).values_list("role__name")
        account_info = {
            "id": account.id,
            "username": account.username,
            "role": [role[0] for role in roles],
            "level": Account.level_list[int(account.level) - 1][1],
            "add_time": account.add_time.strftime('%Y-%m-%d'),
            "is_active": account.is_active
        }
        if not account.department:
            account_info["department"] = ""
        else:
            account_info["department"] = account.department.name
        if not account.company:
            account_info["company"] = ""
        else:
            account_info["company"] = account.company.name
        if not account.position:
            account_info["position"] = ""
        else:
            account_info["position"] = account.position.name
        roles_data.append(account_info)
    role_list = {"data": roles_data, "msg": "", "code": 0, "count": count}
    rdata = json.dumps(role_list)
    return HttpResponse(rdata, content_type="application/json")


def AdminEdit(req, id):
    if req.method == "GET":
        roles = Role.objects.filter(mark=1)
        positions = Position.objects.filter(mark=1)
        departments = Department.objects.filter(mark=1)
        companies = Company.objects.filter(mark=1)
        account = Account.objects.get(id=id)
        account_role = [item["role_id"] for item in account.accountrole_set.values("role_id")]
        return render(req, "admin/admin/admin-edit.html", locals())
    else:
        last_admin_info = Account.objects.get(id=id)
        last_role_list = [item[0] for item in AccountRole.objects.filter(account_id=id).values_list("role_id")]
        response = {"code": 200, "msg": "用户信息修改成功"}
        data = {}
        current_role_list = []
        for k, v in req.POST.items():
            if k != "csrfmiddlewaretoken" and not k.startswith("id"):
                if v:
                    data[k] = v
            if k.startswith("id"):
                current_role_list.append(v)
        add_role_list = set(current_role_list) - set(last_role_list)
        del_role_list = set(last_role_list) - set(current_role_list)
        nochange_role_list = set(current_role_list) & set(last_role_list)
        try:
            with transaction.atomic():
                account_obj = Account.objects.get(id=id)
                account_obj.__dict__.update(**data)
                account_obj.save()
                AccountRole.objects.filter(account_id=account_obj, role__id__in=del_role_list).delete()
                for item in add_role_list:
                    AccountRole.objects.create(role_id=item, account=account_obj)
        except IntegrityError:
            response["code"] = 400
            response["msg"] = "用户名已存在"
        except Exception as e:
            response["code"] = 500
            response["msg"] = "服务器出现未知错误【%s】" % str(e)
        return JsonResponse(response)


def AdminDel(req):
    if req.method == "POST":
        response = {"code": 200, "msg": "用户删除成功"}
        account_list = json.loads(req.POST.get("id"))
        if not isinstance(account_list, list):
            account_list = [account_list, ]
        for account in account_list:
            if Account.objects.filter(id=account, mark=1).first():
                try:
                    with transaction.atomic():
                        Account.objects.filter(id=account).update(mark=0)
                except Exception as e:
                    response["code"] = 500
                    response["msg"] = "服务器出现未知错误【%s】" % str(e)
            else:
                response["code"] = 400
                response["msg"] = "此用户已被删除"
        return JsonResponse(response)


def AccountUpdateStatus(req):
    """
    用户启用状态更新
    :param req:
    :return:
    """
    if req.method == "POST":
        response = {"code": 200, "msg": ""}
        id = req.POST.get("id")
        is_active = json.loads(req.POST.get("is_active"))
        try:
            with transaction.atomic():
                Account.objects.filter(id=id).update(is_active=is_active)
        except Exception as e:
            response["code"] = 500
            response["msg"] = "服务器出现未知错误【%s】" % str(e)
        return JsonResponse(response)
