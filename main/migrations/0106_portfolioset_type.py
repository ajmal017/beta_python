# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0105_portfolioprovider_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='portfolioset',
            name='type',
            field=models.IntegerField(default=2, choices=[(1, 'AON'), (2, 'BetaSmartz'), (3, 'Krane'), (4, 'LEE')]),
        ),
    ]
