# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-22 18:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('avs', '0005_auto_20161022_1603'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='verdict',
            field=models.CharField(default=0, max_length=10),
            preserve_default=False,
        ),
    ]