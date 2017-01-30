# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0098_auto_20170122_1522'),
    ]

    operations = [
        migrations.AddField(
            model_name='portfolio',
            name='rebalance',
            field=models.BooleanField(default=True),
        ),
    ]
