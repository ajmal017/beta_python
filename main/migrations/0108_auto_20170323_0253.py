# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0107_auto_20170323_0154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='portfolioset',
            name='risk_free_rate',
            field=models.FloatField(default=0.0),
        ),
    ]
