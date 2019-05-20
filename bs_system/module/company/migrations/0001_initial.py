# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2019-03-11 13:20
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('addr', models.CharField(default='', max_length=255)),
                ('fax', models.CharField(max_length=255)),
                ('mobile', models.CharField(default='', max_length=255)),
                ('email', models.EmailField(default='', max_length=255)),
                ('tel', models.CharField(default='', max_length=255)),
                ('en_name', models.CharField(default='', max_length=255)),
                ('add_time', models.DateTimeField(default=datetime.datetime(2019, 3, 11, 13, 20, 6, 33901))),
                ('modify_time', models.DateTimeField(auto_now=True)),
                ('mark', models.BooleanField(default=1)),
            ],
            options={
                'db_table': 'bs_system_company',
            },
        ),
    ]
