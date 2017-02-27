# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import main.models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0101_auto_20170223_1936'),
    ]

    operations = [
        migrations.AddField(
            model_name='goal',
            name='portfolio_provider',
            field=models.ForeignKey(default=main.models.get_default_provider_id, to='main.PortfolioProvider', related_name='goal'),
        ),
    ]
