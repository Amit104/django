# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-22 16:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('avs', '0004_solved'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='time_taken',
            field=models.CharField(max_length=10),
        ),
    ]
