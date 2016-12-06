# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('retiresmartz', '0015_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='retirementplaneinc',
            name='amount',
            field=models.FloatField(),
        ),
    ]
