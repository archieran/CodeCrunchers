# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-04-06 14:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evaluation', '0004_auto_20170331_1410'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problem',
            name='model_solution',
            field=models.TextField(verbose_name='Model solution'),
        ),
    ]