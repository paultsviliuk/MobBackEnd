# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-21 15:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='news_information',
            field=models.CharField(max_length=550),
        ),
    ]