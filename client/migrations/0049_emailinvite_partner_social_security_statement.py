# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0048_emailinvite_social_security_statement'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailinvite',
            name='partner_social_security_statement',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]
