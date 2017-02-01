# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('retiresmartz', '0018_retirementplan_balance'),
    ]

    operations = [
        migrations.AddField(
            model_name='retirementplan',
            name='retirement_accounts',
            field=jsonfield.fields.JSONField(blank=True, help_text='List of retirement accounts [{id, name, acc_type, owner, balance, balance_efdt, contrib_amt, contrib_period, employer_match, employer_match_type},...]', null=True),
        ),
    ]
