# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0046_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientaccount',
            name='asset_fee_plan',
            field=models.ForeignKey(to='main.AssetFeePlan'),
        ),
    ]
