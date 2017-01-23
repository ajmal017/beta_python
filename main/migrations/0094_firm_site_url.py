# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0093_auto_20170116_0507'),
    ]

    operations = [
        migrations.AddField(
            model_name='firm',
            name='site_url',
            field=models.CharField(blank=True, max_length=255, default='https://www.betasmartz.com', help_text='Official Site URL', null=True),
        ),
    ]
