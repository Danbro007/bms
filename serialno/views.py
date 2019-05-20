import json
import time
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import SerialNo
import random
from django.db import transaction


# Create your views here.
def SerialNoList(req):
    return render(req, "serialno/serialno-list.html")


def SerialNoData(req):
    page = int(req.GET.get("page"))
    limit = int(req.GET.get("limit"))
    keyword = req.GET.get("keyword")
    if keyword:
        serialnos = SerialNo.objects.filter(sn=keyword)
    else:
        serialnos = SerialNo.objects.all()
    count = serialnos.count()
    serialnos_show = serialnos[(page - 1) * limit:page * limit]
    serialnos_data = []
    for serialno in serialnos_show:
        serialno_info = {
            "id": serialno.id,
            "sn": serialno.sn,
            "is_used": serialno.used_list[serialno.is_used][1],
            "add_time": time.strftime("%Y-%m-%d", time.localtime(float(serialno.add_time)))
        }
        serialnos_data.append(serialno_info)
    SerilNo_list = {"data": serialnos_data, "msg": "", "code": 0, "count": count}
    response_data = json.dumps(SerilNo_list)
    return HttpResponse(response_data, content_type="application/json", )


def SerialNoAdd(req):
    if req.method == "POST":
        response = {"code": 200, "msg": "生成编码成功"}
        add_time = time.time()
        for i in range(20):
            serialno = SerialNo.objects.create(add_time=add_time)
            SerialNo.objects.filter(id=serialno.id).update(sn=get_random_sn(str(serialno.id)))
        return JsonResponse(response)


def SerialNoDel(req):
    if req.method == "POST":
        response = {"code": 200, "msg": "编码删除成功"}
        serialno_list = json.loads(req.POST.get("id"))
        if not isinstance(serialno_list, list):
            serialno_list = [serialno_list, ]
        try:
            with transaction.atomic():
                SerialNo.objects.filter(id__in=serialno_list).delete()
        except Exception as e:
            response["code"] = 500
            response["msg"] = "服务器出现未知问题【%s】" % e
        return JsonResponse(response)




def get_random_sn(id):
    random_alphabet = ""
    random_number = ""
    for i in range(2):
        random_alphabet += chr(random.randint(65, 90))
    for i in range(2):
        random_number += chr(random.randint(48, 57))
    return "".join(["SST", random_number, random_alphabet, id])
