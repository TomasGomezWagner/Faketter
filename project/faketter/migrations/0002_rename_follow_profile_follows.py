# Generated by Django 5.0.5 on 2024-05-20 00:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('faketter', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='follow',
            new_name='follows',
        ),
    ]