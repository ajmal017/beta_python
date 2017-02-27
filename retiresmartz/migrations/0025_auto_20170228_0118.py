# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('retiresmartz', '0024_retirementplaneinc_account_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='retirementprojection',
            name='on_track',
            field=models.BooleanField(help_text='Whether the retirement plan is on track', default=False),
        ),
        migrations.AddField(
            model_name='retirementprojection',
            name='proj_data',
            field=jsonfield.fields.JSONField(help_text='Calculated Projection data for api response', blank=True, null=True),
        ),
    ]
