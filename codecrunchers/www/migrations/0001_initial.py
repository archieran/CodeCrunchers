# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-03-30 04:21
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import www.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_type', models.CharField(choices=[('S', 'Student'), ('C', 'Candidate'), ('E', 'Employer'), ('F', 'Faculty')], default='S', max_length=255)),
                ('user_avatar', models.ImageField(default='profileimages/anonymous.jpg', upload_to=www.models.get_user_avatar_name)),
                ('experience_points', models.IntegerField(default=0, verbose_name='Experience Points')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
