# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0035_auto_20161205_1239'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='student_loan',
            field=models.NullBooleanField(),
        ),
    ]
