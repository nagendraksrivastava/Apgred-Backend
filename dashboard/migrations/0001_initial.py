# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-31 18:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PotentialCustomer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255)),
                ('company_name', models.CharField(max_length=255)),
                ('company_web_url', models.CharField(max_length=255)),
                ('phone_number', models.CharField(max_length=64)),
                ('is_contacted', models.BooleanField(default=False)),
                ('response', models.CharField(max_length=255)),
                ('interest', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
