# Generated by Django 4.2.3 on 2023-08-03 08:01

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookmarks', '0001_initial'),
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='following',
            field=models.ManyToManyField(related_name='followers', through='bookmarks.Contact', to=settings.AUTH_USER_MODEL),
        ),
    ]
