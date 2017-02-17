# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0053_client_employer_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='HealthDevice',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('provider', models.IntegerField(null=True, choices=[(1, 'Google Fit'), (2, 'Fitbit'), (3, 'Samsung Digital Health'), (4, 'Microsoft Health'), (5, 'Jawbone'), (6, 'Under Armour'), (7, 'Withings'), (8, 'TomTom'), (9, 'Garmin')], help_text='Heath device provider')),
                ('token', models.CharField(help_text='Auth Token', max_length=1000)),
                ('refresh_token', models.CharField(null=True, help_text='Auth refresh token', max_length=1000, blank=True)),
                ('expires_at', models.DateTimeField(null=True, help_text='Auth token expiry time', blank=True)),
                ('meta', jsonfield.fields.JSONField(null=True, help_text='Meta data', blank=True)),
                ('client', models.OneToOneField(related_name='health_device', help_text='The health device owner', to='client.Client')),
            ],
        ),
    ]
