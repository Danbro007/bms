from django.db import models
from django.utils import timezone


class Company(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    addr = models.CharField(max_length=255, default="")
    fax = models.CharField(max_length=255)
    mobile = models.CharField(max_length=255, default="")
    email = models.EmailField(max_length=255, default="")
    tel = models.CharField(max_length=255, default="")
    # image = models.CharField(max_length=255, default="")
    en_name = models.CharField(max_length=255, default="")
    add_time = models.DateTimeField(default=timezone.now())
    modify_time = models.DateTimeField(auto_now=True)
    mark = models.BooleanField(default=1)

    class Meta:
        db_table = "bs_system_company"
