from django.db import models
from wechat_app.models import Chatroom


# Create your models here.
class WechatPush(models.Model):
    id = models.AutoField(primary_key=True)
    chatroom = models.ForeignKey(Chatroom)
    push_time = models.CharField(max_length=255)
    content = models.TextField()

    class Meta:
        db_table = "wecaht_wechat_push"
