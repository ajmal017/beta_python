# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('retiresmartz', '0016_auto_20161206_1942'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='retirementadvice',
            name='action',
        ),
        migrations.RemoveField(
            model_name='retirementadvice',
            name='action_data',
        ),
        migrations.RemoveField(
            model_name='retirementadvice',
            name='action_url',
        ),
        migrations.AddField(
            model_name='retirementadvice',
            name='actions',
            field=jsonfield.fields.JSONField(help_text='List of actions [{label, url, data},...]', blank=True, null=True),
        ),
    ]
