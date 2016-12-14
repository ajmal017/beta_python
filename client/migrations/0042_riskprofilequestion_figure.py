# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0041_auto_20161212_1808'),
    ]

    operations = [
        migrations.AddField(
            model_name='riskprofilequestion',
            name='figure',
            field=models.TextField(null=True, blank=True),
        ),
    ]
