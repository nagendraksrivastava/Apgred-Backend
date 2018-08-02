# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-17 07:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('unnayan', '0002_auto_20180616_1732'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appuserinfo',
            name='api_call_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='appuserinfo',
            name='hard_push_ok',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='appuserinfo',
            name='register_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='appuserinfo',
            name='soft_push_cancel_counter',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='appuserinfo',
            name='soft_push_cancel_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='appuserinfo',
            name='soft_push_ok',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
