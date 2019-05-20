# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2019-03-11 13:20
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('code', models.CharField(default='', max_length=50)),
                ('add_time', models.DateTimeField(default=datetime.datetime(2019, 3, 11, 13, 20, 6, 37871))),
                ('modify_time', models.DateTimeField(auto_now=True)),
                ('mark', models.BooleanField(default=1)),
                ('parent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='department.Department')),
            ],
            options={
                'db_table': 'bs_system_department',
            },
        ),
    ]
