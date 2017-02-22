# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-09 23:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0010_auto_20161215_0019'),
    ]

    operations = [
        migrations.AddField(
            model_name='module',
            name='dispatch',
            field=models.CharField(default='none', max_length=200, verbose_name='dispatch'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='module',
            name='internal_name',
            field=models.CharField(default='noname', max_length=200, verbose_name='internal_name'),
            preserve_default=False,
        ),
    ]
