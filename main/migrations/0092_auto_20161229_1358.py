# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0091_merge'),
    ]

    operations = [
        migrations.CreateModel(
            name='ManagerBenchmarks',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('market_index', models.ForeignKey(to='main.MarketIndex')),
                ('ticker', models.ForeignKey(to='main.Ticker')),
            ],
        ),
        migrations.AddField(
            model_name='ticker',
            name='manager_benchmark',
            field=models.ManyToManyField(through='main.ManagerBenchmarks', related_name='manager_tickers', to='main.MarketIndex'),
        ),
        migrations.AlterUniqueTogether(
            name='managerbenchmarks',
            unique_together=set([('ticker', 'market_index')]),
        ),
    ]
