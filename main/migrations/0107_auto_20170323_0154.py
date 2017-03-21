# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import main.models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0106_portfolioset_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='DefaultPortfolioSet',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('changed', models.DateTimeField(auto_now_add=True)),
                ('default_set', models.OneToOneField(blank=True, null=True, to='main.PortfolioSet')),
            ],
        ),
        migrations.AlterField(
            model_name='goal',
            name='portfolio_set',
            field=models.ForeignKey(default=main.models.get_default_set_id, to='main.PortfolioSet', related_name='goal'),
        ),
    ]
