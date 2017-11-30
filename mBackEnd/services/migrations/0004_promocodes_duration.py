# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-16 18:10
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0003_promocodes'),
    ]

    operations = [
        migrations.AddField(
            model_name='promocodes',
            name='duration',
            field=models.IntegerField(default=0, max_length=20),
            preserve_default=False,
        ),
    ]
