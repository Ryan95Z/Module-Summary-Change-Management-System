# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-14 19:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timeline', '0013_notification'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='link',
            field=models.CharField(default='/', max_length=100),
            preserve_default=False,
        ),
    ]
