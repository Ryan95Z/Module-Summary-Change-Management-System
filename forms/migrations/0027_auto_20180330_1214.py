# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-30 11:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_remove_module_seen_by_before'),
        ('forms', '0026_auto_20180329_1908'),
    ]

    operations = [
        migrations.CreateModel(
            name='ModuleChangeSummary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('changes_to_outcomes', models.BooleanField(default=False, verbose_name='Changes to learning outcomes and/or syllabus')),
                ('changes_to_outcomes_desc', models.TextField(blank=True, max_length=750)),
                ('changes_to_teaching', models.BooleanField(default=False, verbose_name='Changes to method of teaching (e.g. number of lectures, labs, tutorials, etc.')),
                ('changes_to_teaching_desc', models.TextField(blank=True, max_length=750)),
                ('changes_to_assessments', models.BooleanField(default=False, verbose_name='Changes to assessments')),
                ('changes_to_assessments_desc', models.TextField(blank=True, max_length=750)),
                ('changes_other', models.BooleanField(default=False, verbose_name='Any other changes')),
                ('changes_other_desc', models.TextField(blank=True, max_length=750)),
                ('changes_rationale', models.TextField(blank=True, max_length=1000, verbose_name='Rationale for changes - please provide a full explanation of the reason for changes')),
                ('archive_flag', models.BooleanField(default=False)),
                ('staging_flag', models.BooleanField(default=False)),
                ('current_flag', models.BooleanField(default=False)),
                ('version_number', models.IntegerField(default=1)),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Module')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='moduleassessment',
            name='version_number',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='modulesoftware',
            name='version_number',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='modulesupport',
            name='version_number',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='moduleteaching',
            name='version_number',
            field=models.IntegerField(default=1),
        ),
    ]