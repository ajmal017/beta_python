# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0047_auto_20170107_0148'),
    ]

    operations = [
        migrations.CreateModel(
            name='BrokerAccount',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('account_id', models.CharField(max_length=32)),
                ('broker', models.CharField(max_length=32)),
                ('bs_account', models.OneToOneField(related_name='broker_account', to='client.ClientAccount')),
            ],
        ),
        migrations.RemoveField(
            model_name='apexaccount',
            name='bs_account',
        ),
        migrations.RemoveField(
            model_name='ibaccount',
            name='bs_account',
        ),
        migrations.DeleteModel(
            name='APEXAccount',
        ),
        migrations.DeleteModel(
            name='IBAccount',
        ),
    ]
