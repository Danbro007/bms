# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2019-03-11 13:22
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('role', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='role',
            name='add_time',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 11, 13, 22, 13, 881252)),
        ),
        migrations.AlterField(
            model_name='roleauth',
            name='add_time',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 11, 13, 22, 13, 882244)),
        ),
    ]
