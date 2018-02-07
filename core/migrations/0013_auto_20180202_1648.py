# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-02 16:48
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20180202_1500'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='reviewer',
            options={'ordering': ['user']},
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['username']},
        ),
        migrations.AddField(
            model_name='reviewer',
            name='modules',
            field=models.ManyToManyField(to='core.Module'),
        ),
        migrations.AddField(
            model_name='reviewer',
            name='user',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='reviewer',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='reviewer',
            name='module',
        ),
        migrations.RemoveField(
            model_name='reviewer',
            name='reviewer_user',
        ),
    ]