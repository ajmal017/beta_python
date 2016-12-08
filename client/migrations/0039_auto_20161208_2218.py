# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0038_clientaccount_account_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='employment_status',
            field=models.IntegerField(blank=True, null=True, choices=[(0, 'Employed'), (1, 'Unmployed'), (2, 'Self-employed'), (3, 'Retired'), (4, 'Not in labor force')]),
        ),
    ]
