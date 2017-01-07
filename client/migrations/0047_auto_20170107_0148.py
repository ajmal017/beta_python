# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0046_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='employee_contributions_last_year',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='client',
            name='employer_contributions_last_year',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='client',
            name='home_growth',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='client',
            name='home_value',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='client',
            name='pension_amount',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='client',
            name='pension_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='client',
            name='pension_start_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='client',
            name='ss_fra_retirement',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='client',
            name='ss_fra_todays',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='client',
            name='state_tax_after_credits',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='client',
            name='state_tax_effrate',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='client',
            name='total_contributions_last_year',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
