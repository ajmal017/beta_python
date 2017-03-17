# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0104_auto_20170310_1457'),
    ]

    operations = [
        migrations.AddField(
            model_name='portfolioprovider',
            name='type',
            field=models.IntegerField(default=2, choices=[(1, 'AON'), (2, 'BetaSmartz'), (3, 'Krane'), (4, 'LEE')], unique=True),
        ),
    ]
