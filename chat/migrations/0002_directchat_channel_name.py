# Generated by Django 2.1.3 on 2019-05-14 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='directchat',
            name='channel_name',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
