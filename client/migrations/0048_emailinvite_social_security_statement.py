# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0047_auto_20170107_0148'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailinvite',
            name='social_security_statement',
            field=models.FileField(null=True, upload_to='', blank=True),
        ),
    ]
