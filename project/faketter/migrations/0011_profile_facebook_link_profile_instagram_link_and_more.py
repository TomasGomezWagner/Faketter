# Generated by Django 5.0.5 on 2024-06-02 21:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faketter', '0010_feek_likes_alter_profile_profile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='facebook_link',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='instagram_link',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='linkedin_link',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='personal_link',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
