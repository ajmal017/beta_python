# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0099_auto_20170210_1153'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='goal',
            name='portfolio_provider',
        ),
    ]
