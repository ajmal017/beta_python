# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0108_auto_20170323_0253'),
    ]

    operations = [
        migrations.AlterField(
            model_name='portfolioprovider',
            name='type',
            field=models.IntegerField(choices=[(1, 'AON'), (2, 'Krane'), (3, 'LEE')], default=2, unique=True),
        ),
        migrations.AlterField(
            model_name='portfolioset',
            name='type',
            field=models.IntegerField(choices=[(1, 'AON'), (2, 'Krane'), (3, 'LEE')], default=2),
        ),
    ]
