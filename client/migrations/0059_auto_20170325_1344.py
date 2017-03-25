# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0058_ibonboard'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ibonboard',
            name='reg_status_stk_cont'
        ),
        migrations.AddField(
            model_name='ibonboard',
            name='reg_status_stk_cont',
            field=models.IntegerField(choices=[(1, 'A Director'), (2, 'A 10% Shareholder'), (3, 'A Policy-Making Officer')], help_text='STKCONTROL', null=True, blank=True),
        ),
    ]
