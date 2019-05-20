from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from bs_system.module.rule.models import Auth


class Role(models.Model):
    level_name = (
        (1, "一级"),
        (2, "二级"),
        (3, "三级"),
    )
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False)
    desc = models.CharField(max_length=255, null=True)
    level = models.SmallIntegerField(default=3, choices=level_name)
    # sort = models.IntegerField(default=5)
    add_time = models.DateTimeField(default=timezone.now())
    modify_time = models.DateTimeField(auto_now=True)
    mark = models.BooleanField(default=1)
    is_active = models.BooleanField(default=1)
    # operate_id = models.IntegerField(default=0)

    class Meta:
        db_table = "bs_system_role"


class RoleAuth(models.Model):
    id = models.AutoField(primary_key=True)
    role = models.ForeignKey(to="Role", to_field="id")
    auth = models.ForeignKey(Auth)
    mark = models.BooleanField(default=1)
    add_time = models.DateTimeField(default=timezone.now())

    class Meta:
        db_table = "bs_system_role_auth"
