# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2019-03-11 13:22
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('department', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='add_time',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 11, 13, 22, 13, 877305)),
        ),
    ]
