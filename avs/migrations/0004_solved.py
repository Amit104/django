# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-07 07:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('avs', '0003_auto_20161007_0450'),
    ]

    operations = [
        migrations.CreateModel(
            name='solved',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('questions', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='avs.Questions')),
                ('users', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='avs.UserProfile')),
            ],
        ),
    ]
