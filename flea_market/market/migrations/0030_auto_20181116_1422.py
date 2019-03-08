# Generated by Django 2.0.4 on 2018-11-16 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0029_auto_20181116_1412'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('typ', models.IntegerField(default=0)),
                ('name', models.CharField(max_length=128)),
                ('description', models.CharField(blank=True, max_length=512)),
                ('picture', models.ImageField(blank=True, null=True, upload_to='goods')),
                ('nums', models.IntegerField(default=0)),
                ('publish_time', models.DateField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='userprofile',
            name='is_tengfei',
            field=models.BooleanField(default=False),
        ),
    ]