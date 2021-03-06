# Generated by Django 2.0.4 on 2018-11-09 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0016_instationmessage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='goods',
            name='discount',
        ),
        migrations.RemoveField(
            model_name='goods',
            name='goods_phone',
        ),
        migrations.RemoveField(
            model_name='goods',
            name='goods_qq',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='height',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='width',
        ),
        migrations.AddField(
            model_name='goods',
            name='typ',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='mail',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='nums',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='phone',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
