# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import main.models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0100_remove_goal_portfolio_provider'),
    ]

    operations = [
        migrations.AddField(
            model_name='goal',
            name='portfolio_provider',
            field=models.ForeignKey(to='main.PortfolioProvider', related_name='goal', blank=True, default=main.models.get_default_provider_id, null=True),
        ),
        migrations.AlterField(
            model_name='defaultportfolioprovider',
            name='default_provider',
            field=models.OneToOneField(to='main.PortfolioProvider', blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='portfolioprovider',
            name='TLH',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='portfolioprovider',
            name='portfolio_optimization',
            field=models.BooleanField(default=True),
        ),
    ]
