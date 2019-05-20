from django.db import models
from django.utils import timezone
from bs_system.module.company.models import Company



class Position(models.Model):
    level_name = (
        (1, "管理员"),
        (2, "负责人"),
        (3, "员工")
    )
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    level = models.IntegerField(default=3, choices=level_name, )
    add_time = models.DateTimeField(default=timezone.now())
    modify_time = models.DateTimeField(auto_now=True)
    mark = models.BooleanField(default=1)

    class Meta:
        db_table = "bs_system_postion"
