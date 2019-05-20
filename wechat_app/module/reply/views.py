import json
import os
from django.shortcuts import render
from wechat_app.models import *
from django.http import HttpResponse, JsonResponse
from django.db import transaction
from wechat.settings import UPLOADFILES_DIR
from django.db.utils import IntegrityError

import hashlib


# Create your views here.
def ReplyList(req):
    return render(req, "wechat/reply/list.html", locals())


def ReplyData(req):
    page = int(req.GET.get("page"))
    limit = int(req.GET.get("limit"))
    keyword = req.GET.get("keyword")
    if keyword:
        reply_all = Reply.objects.filter(keyword__contains=keyword).all()
    else:
        reply_all = Reply.objects.all()
    count = reply_all.count()
    reply_list = reply_all[(page - 1) * limit:page * limit]
    reply_msg_data = []
    for reply in reply_list:
        chatrooms = ReplyToChatroom.objects.filter(reply=reply).values("chatroom__nickname", "msg", "filename")
        if chatrooms:
            reply_info = {
                "id": reply.id,
                "keyword": reply.keyword,
                "type": reply.type_list[reply.type - 1][1],
                "chatrooms": [chatroom["chatroom__nickname"] for chatroom in chatrooms]
            }
            if reply.type == 1:
                reply_info["reply"] = chatrooms.first()["msg"]
            else:
                reply_info["reply"] = chatrooms.first()["filename"]
            reply_msg_data.append(reply_info)
    Replay_list = {"data": reply_msg_data, "msg": "", "code": 0, "count": count}
    rdata = json.dumps(Replay_list)
    return HttpResponse(rdata, content_type="application/json", )


def ReplyAdd(req):
    if req.method == "GET":
        reply = Reply
        chatrooms = Chatroom.objects.all()
        return render(req, "wechat/reply/add.html", locals())
    else:
        response = {"code": 200, "msg": "回复消息添加成功"}
        keyword = req.POST.get("keyword")
        msg = req.POST.get("msg")
        type = req.POST.get("type")
        filename = req.POST.get("filename")
        chatroom_list = req.POST.get("chatroom").split(",")
        if not keyword:
            response["code"] = 401
            response["msg"] = "请输入关键词"
        else:
            if type == "1":
                if not msg:
                    response["code"] = 402
                    response["msg"] = "请输入回复语句"
                else:
                    repeat_keyword_chatrooms = []
                    try:
                        with transaction.atomic():
                            reply_obj = Reply.objects.create(keyword=keyword, type=type)
                            for chatroom in chatroom_list:
                                if not ReplyToChatroom.objects.filter(chatroom_id=chatroom, reply__keyword=keyword):
                                    ReplyToChatroom.objects.create(chatroom_id=chatroom, reply=reply_obj, msg=msg)
                                else:
                                    repeat_keyword_chatrooms.append(
                                        "【" + Chatroom.objects.get(id=chatroom).nickname + "】")
                            if repeat_keyword_chatrooms:
                                raise IntegrityError
                    except IntegrityError:
                        response["code"] = 403
                        response["msg"] = "微信群%s已存在关键字【%s】" % ("".join(repeat_keyword_chatrooms), keyword)
                    except Exception as e:
                        response["code"] = 500
                        response["msg"] = "服务器出现未知错误【%s】" % e
            else:
                if not filename:
                    response["code"] = 403
                    response["msg"] = "请选择上传内容"
                else:
                    repeat_keyword_chatrooms = []
                    try:
                        with transaction.atomic():
                            filepath = os.path.join(UPLOADFILES_DIR, filename_hash(filename))
                            reply_obj = Reply.objects.create(keyword=keyword, type=type)
                            for chatroom in chatroom_list:
                                if not ReplyToChatroom.objects.filter(chatroom_id=chatroom, reply__keyword=keyword):
                                    ReplyToChatroom.objects.create(chatroom_id=chatroom, reply=reply_obj,
                                                                   filename=filename,
                                                                   filepath=filepath)
                                else:
                                    repeat_keyword_chatrooms.append(
                                        "【" + Chatroom.objects.get(id=chatroom).nickname + "】")
                            if repeat_keyword_chatrooms:
                                raise IntegrityError
                    except IntegrityError:
                        response["code"] = 403
                        response["msg"] = "微信群%s已存在关键字【%s】" % ("".join(repeat_keyword_chatrooms), keyword)
                    except Exception as e:
                        response["code"] = 500
                        response["msg"] = "服务器出现未知错误【%s】" % e
        return JsonResponse(response)


def ReplyEdit(req, id):
    if req.method == "GET":
        reply = Reply.objects.get(id=id)
        msg = ReplyToChatroom.objects.filter(reply_id=reply).values_list("msg").first()[0]
        have_chatrooms = [item["chatroom_id"] for item in
                          ReplyToChatroom.objects.filter(reply_id=id).values("chatroom_id")]
        chatrooms = Chatroom.objects.all()
        return render(req, "wechat/reply/edit.html", locals())
    else:
        response = {"code": 200, "msg": "回复消息修改成功"}
        keyword = req.POST.get("keyword")
        msg = req.POST.get("msg")
        type = req.POST.get("type")
        filename = req.POST.get("filename")
        last_keyword_chatrooms = [item["chatroom__id"] for item in
                                  ReplyToChatroom.objects.filter(reply_id=id).values("chatroom__id")]
        current_keyword_chatrooms = [int(item) for item in req.POST.get("chatroom").split(",")]
        add_keyword_chatrooms = set(current_keyword_chatrooms) - set(last_keyword_chatrooms)
        delete_keyword_chatrooms = set(last_keyword_chatrooms) - set(current_keyword_chatrooms)
        no_change_keyword_chatrooms = set(last_keyword_chatrooms) & set(current_keyword_chatrooms)
        if not keyword:
            response["code"] = 402
            response["msg"] = "请输入关键词"
            return response
        reply_obj = Reply.objects.get(id=id)  # 原来的回复消息对象
        filepath = ReplyToChatroom.objects.filter(reply_id=id).values_list("filepath").first()[0]
        if type == "1":  # 文字
            if not msg:
                response["code"] = 403
                response["msg"] = "请输入回复语句"
            else:
                repeat_keyword_chatrooms = []
                data = {"keyword": keyword, "type": type}
                try:
                    with transaction.atomic():
                        reply_obj.__dict__.update(**data)
                        reply_obj.save()
                        for chatroom in current_keyword_chatrooms:
                            if not ReplyToChatroom.objects.filter(chatroom_id=chatroom, reply__keyword=keyword).exclude(
                                    reply_id=id):
                                if not ReplyToChatroom.objects.filter(chatroom_id=chatroom, reply_id=id):
                                    ReplyToChatroom.objects.create(chatroom_id=chatroom, reply_id=id, msg=msg)
                                else:
                                    ReplyToChatroom.objects.filter(chatroom_id=chatroom, reply_id=id).update(msg=msg,
                                                                                                             filename="",
                                                                                                             filepath="")
                            else:
                                repeat_keyword_chatrooms.append("【" + Chatroom.objects.get(id=chatroom).nickname + "】")
                        if repeat_keyword_chatrooms:
                            raise IntegrityError
                        if filepath:
                            os.remove(filepath)
                        ReplyToChatroom.objects.filter(chatroom__id__in=delete_keyword_chatrooms, reply_id=id).delete()
                except IntegrityError:
                    response["code"] = 403
                    response["msg"] = "微信群%s已存在关键字【%s】" % ("".join(repeat_keyword_chatrooms), keyword)
                except Exception as e:
                    response["code"] = 500
                    response["msg"] = "服务器出现未知错误【%s】" % e
        else:  # 文件或者图片
            repeat_keyword_chatrooms = []
            data = {"keyword": keyword, "type": type}  # 关键词修改
            try:
                with transaction.atomic():
                    reply_obj.__dict__.update(**data)
                    reply_obj.save()
                    for chatroom in current_keyword_chatrooms:
                        if not ReplyToChatroom.objects.filter(chatroom_id=chatroom, reply__keyword=keyword).exclude(
                                reply_id=id):
                            if not ReplyToChatroom.objects.filter(chatroom_id=chatroom, reply_id=id):
                                ReplyToChatroom.objects.create(chatroom_id=chatroom, reply_id=id, filename=filename,
                                                               filepath=os.path.join(UPLOADFILES_DIR,
                                                                                     filename_hash(filename)))
                            else:
                                ReplyToChatroom.objects.filter(chatroom_id=chatroom, reply_id=id).update(
                                    filename=filename,
                                    filepath=os.path.join(
                                        UPLOADFILES_DIR,
                                        filename_hash(filename)))
                        else:
                            repeat_keyword_chatrooms.append("【" + Chatroom.objects.get(id=chatroom).nickname + "】")
                    if repeat_keyword_chatrooms:
                        raise IntegrityError
                    if filepath:
                        os.remove(filepath)
                    ReplyToChatroom.objects.filter(chatroom__id__in=delete_keyword_chatrooms, reply_id=id).delete()
            except IntegrityError:
                response["code"] = 403
                response["msg"] = "微信群%s已存在关键字【%s】" % ("".join(repeat_keyword_chatrooms), keyword)
            except Exception as e:
                response["code"] = 500
                response["msg"] = "服务器出现未知错误【%s】" % e
        return JsonResponse(response)


def ReplyDel(req):
    if req.method == "POST":
        response = {"code": 200, "msg": "回复信息删除成功"}
        msg_list = json.loads(req.POST.get("id"))
        if not isinstance(msg_list, list):
            msg_list = [msg_list, ]
        for msg in msg_list:
            try:
                with transaction.atomic():
                    reply_obj = Reply.objects.get(id=msg)
                    if reply_obj.type != 1:
                        os.remove(ReplyToChatroom.objects.filter(reply_id=msg).values_list("filepath").first()[0])
                        ReplyToChatroom.objects.filter(reply_id=reply_obj).delete()
                    reply_obj.delete()
            except Exception as e:
                response["code"] = 500
                response["msg"] = "服务器出现未知错误【%s】" % e
        return JsonResponse(response)


def UploadFile(req):
    if req.method == "POST":
        response = {"code": 200, "msg": "上传成功"}
        uploadfile = req.FILES.get("file")
        with open(os.path.join(UPLOADFILES_DIR, filename_hash(uploadfile.name)), "wb") as f:
            for chunk in uploadfile.chunks():
                f.write(chunk)
        response["filename"] = uploadfile.name
        return JsonResponse(response)


def isfile_exist(filename):
    if os.path.exists(os.path.join(UPLOADFILES_DIR, filename_hash(filename))):
        return True
    else:
        return False


def filename_hash(filename):
    name, ext = filename.rsplit(".", 1)
    m = hashlib.md5()
    m.update(name.encode("utf-8"))
    new_name = m.hexdigest()
    return ".".join([new_name, ext])
