# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0109_auto_20170324_0828'),
    ]

    operations = [
        migrations.AlterField(
            model_name='portfolioprovider',
            name='type',
            field=models.IntegerField(default=2, choices=[(1, 'AON'), (2, 'Krane'), (3, 'LEE')]),
        ),
    ]
