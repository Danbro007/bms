# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2019-04-14 21:34
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0006_auto_20190404_1553'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='add_time',
            field=models.DateTimeField(default=datetime.datetime(2019, 4, 14, 21, 34, 6, 35087)),
        ),
    ]
