# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0086_auto_20161220_0637'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goal',
            name='state',
            field=models.IntegerField(choices=[(0, 'Active'), (1, 'Archive Requested'), (2, 'Closing'), (3, 'Archived')], default=0),
        ),
    ]
