# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2019-04-04 15:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wechat_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='replytochatroom',
            name='filename',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='replytochatroom',
            name='filepath',
            field=models.FileField(default='', upload_to='uploadfile/'),
        ),
        migrations.AlterField(
            model_name='replytochatroom',
            name='msg',
            field=models.TextField(default=''),
        ),
    ]
