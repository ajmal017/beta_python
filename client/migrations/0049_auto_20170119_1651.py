# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0048_auto_20170119_1350'),
    ]

    operations = [
        migrations.CreateModel(
            name='APEXAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('apex_account', models.CharField(max_length=32)),
                ('bs_account', models.OneToOneField(related_name='apex_account', to='client.ClientAccount')),
            ],
        ),
        migrations.CreateModel(
            name='IBAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('ib_account', models.CharField(max_length=32)),
                ('bs_account', models.OneToOneField(related_name='ib_account', to='client.ClientAccount')),
            ],
        ),
        migrations.RemoveField(
            model_name='brokeraccount',
            name='bs_account',
        ),
        migrations.DeleteModel(
            name='BrokerAccount',
        ),
    ]
