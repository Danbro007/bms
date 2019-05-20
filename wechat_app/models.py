from django.db import models
from django.utils import timezone


class Chatroom(models.Model):
    id = models.AutoField(primary_key=True)
    nickname = models.CharField(max_length=120, unique=True)
    start_time = models.IntegerField()
    end_time = models.IntegerField()
    remark = models.CharField(max_length=150, null=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = "wechat_chatroom_chatroom"


class Reply(models.Model):
    type_list = (
        (1, "文字"),
        (2, "图片"),
        (3, "文件"),
    )
    id = models.AutoField(primary_key=True)
    keyword = models.CharField(max_length=255, null=False)
    type = models.IntegerField(null=False, choices=type_list)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = "wechat_reply"


class ReplyToChatroom(models.Model):
    id = models.AutoField(primary_key=True)
    reply = models.ForeignKey(to="Reply", to_field="id")
    chatroom = models.ForeignKey(to="Chatroom", to_field="id")
    msg = models.TextField(default="")
    filename = models.CharField(max_length=255, default="")
    filepath = models.FileField(upload_to="uploadfile/", default="")

    class Meta:
        unique_together = (("chatroom", "reply"),)
        db_table = "wechat_reply_to_chatroom"
