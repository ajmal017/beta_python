# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0040_merge'),
    ]

    operations = [
        migrations.CreateModel(
            name='CloseAccountRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('close_choice', models.IntegerField(null=True, choices=[(0, 'Liquidate assets'), (1, 'Transfer assets to another account'), (2, 'Transfer assets to another custodian'), (3, 'Take direct custody of your assets')])),
                ('account_transfer_form', models.FileField(upload_to='', blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='clientaccount',
            name='status',
            field=models.IntegerField(default=0, choices=[(0, 'Open'), (1, 'Pending Close From Admin'), (2, 'Closed')], null=True),
        ),
        migrations.AddField(
            model_name='closeaccountrequest',
            name='account',
            field=models.ForeignKey(to='client.ClientAccount'),
        ),
    ]
