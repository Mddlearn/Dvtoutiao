# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-22 07:53
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='poll_article',
            new_name='Pollarticle',
        ),
    ]