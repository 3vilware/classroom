# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-11-26 01:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Classroom', '0003_auto_20181125_1703'),
    ]

    operations = [
        migrations.AlterField(
            model_name='curso',
            name='codigo',
            field=models.CharField(max_length=10, unique=True),
        ),
    ]
