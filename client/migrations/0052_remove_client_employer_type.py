# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0051_auto_20170125_0756'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='employer_type',
        ),
    ]
