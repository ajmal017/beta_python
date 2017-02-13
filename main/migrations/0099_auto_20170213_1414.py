# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import main.models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0098_auto_20170122_1522'),
    ]

    operations = [
        migrations.CreateModel(
            name='DefaultPortfolioProvider',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('changed', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='PortfolioProvider',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=100)),
                ('TLH', models.BooleanField(default=True)),
                ('portfolio_optimization', models.BooleanField(default=True)),
                ('constants', models.BooleanField(default=True)),
            ],
        ),
        migrations.AddField(
            model_name='defaultportfolioprovider',
            name='default_provider',
            field=models.OneToOneField(to='main.PortfolioProvider', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='goal',
            name='portfolio_provider',
            field=models.ForeignKey(to='main.PortfolioProvider', related_name='goal', default=main.models.get_default_provider_id),
        ),
    ]
