# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0079_auto_20161203_0331'),
    ]

    operations = [
        migrations.AlterField(
            model_name='externalassettransfer',
            name='amount',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='recurringtransaction',
            name='amount',
            field=models.FloatField(),
        ),
    ]
