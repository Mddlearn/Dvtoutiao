# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-23 06:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0003_publicsignal_desc'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='summary',
            field=models.TextField(blank=True),
        ),
    ]
