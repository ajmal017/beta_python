# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0050_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apexaccount',
            name='bs_account',
            field=models.OneToOneField(null=True, to='client.ClientAccount', related_name='apex_account'),
        ),
        migrations.AlterField(
            model_name='ibaccount',
            name='bs_account',
            field=models.OneToOneField(null=True, to='client.ClientAccount', related_name='ib_account'),
        ),
    ]
