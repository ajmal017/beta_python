# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0055_auto_20170223_1936'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='healthdevice',
            name='token',
        ),
        migrations.AddField(
            model_name='healthdevice',
            name='access_token',
            field=models.CharField(max_length=2000, default='', help_text='OAuth access Token'),
        ),
        migrations.AlterField(
            model_name='healthdevice',
            name='expires_at',
            field=models.DateTimeField(null=True, help_text='OAuth token expiry time', blank=True),
        ),
        migrations.AlterField(
            model_name='healthdevice',
            name='refresh_token',
            field=models.CharField(max_length=1000, null=True, help_text='OAuth refresh token', blank=True),
        ),
    ]
