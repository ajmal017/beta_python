# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0052_remove_client_employer_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='employer_type',
            field=models.IntegerField(blank=True, null=True, choices=[(0, 'For-profit business (100+ employees)'), (1, 'For-profit business (up to 100 employees)'), (2, 'For-profit business (only business owner and spouse)'), (3, 'Non-profit private organization'), (4, 'Non-profit public organization'), (5, 'Government (Local, State, Federal)')]),
        ),
    ]
