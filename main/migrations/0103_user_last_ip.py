# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0102_goal_portfolio_provider'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='last_ip',
            field=models.CharField(null=True, blank=True, help_text='Last requested IP address', max_length=20),
        ),
    ]
