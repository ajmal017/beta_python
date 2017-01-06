# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('retiresmartz', '0017_auto_20161207_1509'),
    ]

    operations = [
        migrations.AddField(
            model_name='retirementplan',
            name='balance',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
