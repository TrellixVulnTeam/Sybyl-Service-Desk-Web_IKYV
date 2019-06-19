# Generated by Django 2.1.3 on 2019-05-16 15:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0007_auto_20190516_1810'),
    ]

    operations = [
        migrations.AlterField(
            model_name='directchat',
            name='chat_room_id',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='directchatmessage',
            name='direct_chat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chat.DirectChat'),
        ),
        migrations.AlterField(
            model_name='directchatmessage',
            name='sent_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='directchatmessagereply',
            name='direct_chat_message',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chat.DirectChatMessage'),
        ),
    ]
