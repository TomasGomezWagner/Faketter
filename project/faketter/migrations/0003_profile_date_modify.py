# Generated by Django 5.0.5 on 2024-05-20 01:01

import django.contrib.auth.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faketter', '0002_rename_follow_profile_follows'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='date_modify',
            field=models.DateTimeField(auto_now=True, verbose_name=django.contrib.auth.models.User),
        ),
    ]