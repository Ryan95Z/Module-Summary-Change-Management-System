# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-15 12:37
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_merge_20180222_1205'),
        ('timeline', '0014_notification_link'),
    ]

    operations = [
        migrations.CreateModel(
            name='Watcher',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('watching', models.ManyToManyField(to='core.Module')),
            ],
        ),
    ]