# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0080_auto_20161206_1942'),
    ]

    operations = [
        migrations.AddField(
            model_name='assetfeature',
            name='upper_limit',
            field=models.FloatField(null=True, blank=True, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(1.0)]),
        ),
    ]
