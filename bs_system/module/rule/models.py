from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from bs_system.module.department.models import Department


class Auth(models.Model):
    app_name = (
        "admin/company",
        "admin/department",
        "admin/position",
        "wechat/reply",
        "wechat/chatroom",
        "serialno/serialno",
    )
    act_name = (
        "list",
        "add",
        "edit",
        "delete"
    )
    level_name = (
        (0, "一级"),
        (1, "二级")
    )

    menu_name = (
        (0, "否"),
        (1, "是")
    )
    public_name = (
        (0, "否"),
        (1, "是")
    )
    id = models.AutoField(primary_key=True)
    parent = models.ForeignKey("self", to_field="id", null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, null=False)
    is_public = models.BooleanField(default=0, choices=public_name)
    is_menu = models.BooleanField(default=0, choices=menu_name)
    level = models.BooleanField(default=1, choices=level_name)
    permission_url = models.CharField(max_length=255, default="")
    app = models.CharField(max_length=255, null=False)
    act = models.CharField(max_length=255, null=True)
    mark = models.BooleanField(default=1)
    # parameters = models.CharField(max_length=255, default="")
    # sort = models.IntegerField(default=5)
    add_time = models.DateTimeField(default=timezone.now())
    modify_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "bs_system_auth"
