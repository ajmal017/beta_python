# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('retiresmartz', '0022_auto_20170217_0530'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='retirementprojection',
            name='part_reverse_mort',
        ),
    ]
