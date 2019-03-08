# Generated by Django 2.0.4 on 2018-11-10 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0022_userprofile_description'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='name',
            new_name='family_name',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='given_name',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
