# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-04-03 17:39
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('codeconsole', '0002_auto_20170330_2204'),
    ]

    operations = [
        migrations.CreateModel(
            name='SavedCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.TextField(help_text='Code committed by the user', verbose_name='Code')),
                ('user', models.ForeignKey(help_text='Writer of the code', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Coder')),
            ],
        ),
    ]
