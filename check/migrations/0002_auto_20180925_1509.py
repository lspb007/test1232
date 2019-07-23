# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2018-09-25 15:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        ('check', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='department2system',
            name='d',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Department', verbose_name='巡检科室'),
        ),
        migrations.AddField(
            model_name='department2system',
            name='s',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='check.SystemInfo', verbose_name='业务系统'),
        ),
    ]
