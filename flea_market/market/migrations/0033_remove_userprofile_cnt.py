# Generated by Django 2.0.4 on 2018-11-17 13:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0032_auto_20181117_1408'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='cnt',
        ),
    ]
