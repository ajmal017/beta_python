# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0037_auto_20161205_2340'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientaccount',
            name='account_number',
            field=models.CharField(max_length=16, blank=True, null=True),
        ),
    ]
