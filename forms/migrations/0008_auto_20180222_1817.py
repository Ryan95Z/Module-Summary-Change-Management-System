# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-22 18:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_merge_20180222_1205'),
        ('forms', '0007_auto_20180222_1515'),
    ]

    operations = [
        migrations.CreateModel(
            name='ModuleDescription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='ModuleDescriptionEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('boolean_entry', models.BooleanField()),
                ('string_entry', models.CharField(blank=True, max_length=2000)),
                ('integer_entry', models.IntegerField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='ModuleDescriptionFormVersion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateField()),
            ],
        ),
        migrations.AlterModelOptions(
            name='formfieldentity',
            options={'ordering': ['entity_order']},
        ),
        migrations.AddField(
            model_name='formfieldentity',
            name='entity_order',
            field=models.PositiveSmallIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='moduledescriptionentry',
            name='field_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forms.FormFieldEntity'),
        ),
        migrations.AddField(
            model_name='moduledescription',
            name='entries',
            field=models.ManyToManyField(to='forms.ModuleDescriptionEntry'),
        ),
        migrations.AddField(
            model_name='moduledescription',
            name='form_version',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forms.ModuleDescriptionFormVersion'),
        ),
        migrations.AddField(
            model_name='moduledescription',
            name='module_code',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Module'),
        ),
        migrations.AlterUniqueTogether(
            name='moduledescription',
            unique_together=set([('module_code', 'form_version')]),
        ),
    ]
