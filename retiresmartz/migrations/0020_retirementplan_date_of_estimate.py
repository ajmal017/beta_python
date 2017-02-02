# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('retiresmartz', '0019_retirementplan_retirement_accounts'),
    ]

    operations = [
        migrations.AddField(
            model_name='retirementplan',
            name='date_of_estimate',
            field=models.DateField(null=True, blank=True),
        ),
    ]
