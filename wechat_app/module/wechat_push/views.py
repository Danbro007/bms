import json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from wechat_app.models import *
from .models import WechatPush
# from itchat_part.itchat_run import sched,bot
from django.db import transaction
import time


def wechat_task(nickname, content):
    print(nickname, content)
    group = bot.groups().search(nickname)[0]
    group.send(content)


# Create your views here.
def PushList(req):
    print(sched.get_jobs())
    return render(req, "wechat/push/list.html")


def PushAdd(req):
    if req.method == "GET":
        chatrooms = Chatroom.objects.all()
        return render(req, "wechat/push/add.html", locals())
    else:
        response = {"code": 200, "msg": "推送消息添加成功"}
        data = {}
        for k, v in req.POST.items():
            if k != "csrfmiddlewaretoken":
                data[k] = v
        chatroom = Chatroom.objects.get(id=data["chatroom_id"])
        nickname = chatroom.nickname
        content = data["content"]
        push_obj = WechatPush.objects.create(**data)
        hour, minute, second = data["push_time"].split(":")
        start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(chatroom.start_time))
        end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(chatroom.end_time))
        sched.add_job(wechat_task, "cron", args=[nickname, content], hour=hour, minute=minute, second=second,
                      id=str(push_obj.id))
        return JsonResponse(response)


def PushData(req):
    page = int(req.GET.get("page"))
    limit = int(req.GET.get("limit"))
    pushs = WechatPush.objects
    count = pushs.count()
    push_list = pushs.all()[(page - 1) * limit:page * limit]
    push_data = []
    for push in push_list:
        push_info = {
            "id": push.id,
            "chatroom": push.chatroom.nickname,
            "push_time": push.push_time,
            "content": push.content,
        }
        push_data.append(push_info)
    Push_list = {"data": push_data, "msg": "", "code": 0, "count": count}
    rdata = json.dumps(Push_list)
    return HttpResponse(rdata, content_type="application/json", )


def PushDel(req):
    if req.method == "POST":
        response = {"code": 200, "msg": "推送消息删除成功"}
        push_list = json.loads(req.POST.get("id"))
        if not isinstance(push_list, list):
            push_list = [push_list, ]
        for push in push_list:
            try:
                with transaction.atomic():
                    WechatPush.objects.get(id=push).delete()
                    sched.remove_job(str(push))
            except Exception as e:
                response["code"] = 500
                response["msg"] = "服务器出现未知【%s】错误" % e
        return JsonResponse(response)


def PushEdit(req, id):
    if req.method == "GET":
        chatroom_list = Chatroom.objects.all()
        push = WechatPush.objects.get(id=id)
        return render(req, "wechat/push/edit.html", locals())
    else:
        response = {"code": 200, "msg": "修改成功"}
        data = {}
        for k, v in req.POST.items():
            if k != "csrfmiddlewaretoken":
                data[k] = v
        try:
            with transaction.atomic():
                push_obj = WechatPush.objects.get(id=id)
                push_obj.__dict__.update(**data)
                push_obj.save()
                nickname = push_obj.chatroom.nickname
                content = data["content"]
                hour, minute, second = data["push_time"].split(":")
                sched.remove_job(id)
                start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(push_obj.chatroom.start_time))
                end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(push_obj.chatroom.end_time))
                sched.add_job(wechat_task, "cron", args=[nickname, content], hour=hour, minute=minute, second=second,
                              id=str(push_obj.id))
        except Exception as e:
            response["code"] = 500
            response["msg"] = "服务器出现未知【%s】错误" % e
    return JsonResponse(response)
