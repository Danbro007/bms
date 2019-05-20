from django.db import models


# Create your models here.


class SerialNo(models.Model):
    used_list = (
        (0, "否"),
        (1, "是"),
    )
    id = models.AutoField(primary_key=True)
    sn = models.CharField(max_length=32, null=False)
    add_time = models.CharField(max_length=32, null=False)
    is_used = models.BooleanField(default=0, choices=used_list)

    class Meta:
        db_table = "serialno_serialno"
