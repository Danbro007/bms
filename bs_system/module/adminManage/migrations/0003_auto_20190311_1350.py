# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2019-03-11 13:50
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminManage', '0002_auto_20190311_1322'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='add_time',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 11, 13, 50, 52, 127209)),
        ),
        migrations.AlterField(
            model_name='accountrole',
            name='add_time',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 11, 13, 50, 52, 129689)),
        ),
    ]
