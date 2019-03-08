# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-08 02:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0011_auto_20161207_1407'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='picture_url',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(blank=True, upload_to='profile'),
        ),
    ]
