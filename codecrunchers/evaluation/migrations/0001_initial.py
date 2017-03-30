# -*- coding: utf-8 -*-
<<<<<<< HEAD
# Generated by Django 1.10.4 on 2017-03-30 04:21
=======
# Generated by Django 1.10.4 on 2017-03-30 04:12
>>>>>>> 23e143b810f01ad69a92b3141a0cfca946c3e6e4
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('codeconsole', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Contest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Contest title')),
                ('description', models.TextField(verbose_name='Description')),
                ('start_time', models.DateTimeField(verbose_name='Start time')),
                ('end_time', models.DateTimeField(verbose_name='End time')),
                ('is_active', models.BooleanField(default=False, verbose_name='Active')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Contest Creator')),
            ],
        ),
        migrations.CreateModel(
            name='LiveCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('console_data', models.TextField(verbose_name='Code')),
                ('console_lang', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='codeconsole.ConsoleLanguage')),
                ('live_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('desc', models.CharField(max_length=65535, verbose_name='Description')),
                ('model_solution', models.CharField(max_length=65535, verbose_name='Model solution')),
                ('constraints', models.TextField(max_length=255, verbose_name='Constraints')),
                ('input_format', models.TextField(max_length=255, verbose_name='Input format')),
                ('output_format', models.TextField(max_length=255, verbose_name='Output format')),
                ('startup_code', models.TextField(max_length=65535, verbose_name='Initial code')),
                ('start_time', models.DateTimeField(verbose_name='Problem start time')),
                ('end_time', models.DateTimeField(verbose_name='Problem end time')),
                ('is_practice', models.BooleanField(default=False, verbose_name='Practice Problem')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
                ('difficulty', models.CharField(choices=[('E', 'Easy'), ('M', 'Medium'), ('H', 'Hard'), ('X', 'Expert')], default='E', max_length=255)),
                ('reward_points', models.IntegerField(default=100, verbose_name='Reward points')),
                ('contest', models.ManyToManyField(blank=True, to='evaluation.Contest')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Problem creator')),
            ],
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('submitted_code', models.TextField(verbose_name='Submitted code')),
                ('achieved_score', models.IntegerField(verbose_name='Achieved score')),
                ('total_memory_used', models.IntegerField(verbose_name='Total memory used')),
                ('total_execution_time', models.FloatField(verbose_name='Total execution time')),
                ('attempted', models.DateTimeField(verbose_name='Attempted')),
                ('lang', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='codeconsole.ConsoleLanguage')),
                ('prob', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='evaluation.Problem', verbose_name='Problem')),
                ('sub_made_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
        ),
        migrations.CreateModel(
            name='TestCase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('input_sequence', models.TextField(verbose_name='Expected Input')),
                ('output_sequence', models.TextField(verbose_name='Expected output')),
                ('score', models.IntegerField()),
                ('is_sample', models.BooleanField(default=False, verbose_name='Sample test case')),
                ('problem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='evaluation.Problem', verbose_name='Problem')),
            ],
        ),
        migrations.CreateModel(
            name='TestCaseResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('P', 'PASS'), ('F', 'FAIL')], default='F', max_length=1, verbose_name='Status')),
                ('time_submitted', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Time_Stamp')),
                ('submission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='evaluation.Submission', verbose_name='Submission')),
                ('test_case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='evaluation.TestCase', verbose_name='Test_Case')),
            ],
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic_name', models.CharField(max_length=255, verbose_name='Topic')),
            ],
        ),
        migrations.AddField(
            model_name='problem',
            name='topic',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='evaluation.Topic'),
        ),
    ]
