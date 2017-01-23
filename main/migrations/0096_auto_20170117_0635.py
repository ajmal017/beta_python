# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0095_auto_20170117_0634'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='firm',
            name='site_url',
        ),
        migrations.AddField(
            model_name='firmdata',
            name='site_url',
            field=models.CharField(help_text='Official Site URL', null=True, blank=True, max_length=255, default='https://www.betasmartz.com'),
        ),
    ]
