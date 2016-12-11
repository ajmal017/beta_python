# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0038_clientaccount_account_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountBeneficiary',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('type', models.IntegerField(null=True, choices=[(0, 'Primary'), (1, 'Contingent')])),
                ('name', models.CharField(max_length=255)),
                ('relationship', models.IntegerField(null=True, choices=[(0, 'Legal entity (e.g. charity)'), (1, 'Family member/friend'), (2, 'Spouse'), (3, 'My estate')])),
                ('birthdate', models.DateField()),
                ('share', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(1.0)])),
                ('account', models.ForeignKey(to='client.ClientAccount')),
            ],
        ),
    ]
