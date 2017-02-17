# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0099_portfolio_rebalance'),
    ]

    operations = [
        migrations.CreateModel(
            name='DefaultPortfolioProvider',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('changed', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='PortfolioProvider',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('TLH', models.BooleanField(default=True)),
                ('portfolio_optimization', models.BooleanField(default=True)),
                ('constraints', models.BooleanField(default=True)),
            ],
        ),
        migrations.AddField(
            model_name='defaultportfolioprovider',
            name='default_provider',
            field=models.OneToOneField(null=True, to='main.PortfolioProvider', blank=True),
        ),
    ]
