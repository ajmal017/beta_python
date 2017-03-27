# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0059_auto_20170325_1344'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='hsa_coverage_type',
            field=models.CharField(choices=[('Single', 'Single'), ('Family', 'Family')], blank=True, null=True, max_length=32),
        ),
        migrations.AddField(
            model_name='client',
            name='hsa_eligible',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='client',
            name='hsa_provider_name',
            field=models.CharField(blank=True, null=True, max_length=255),
        ),
        migrations.AddField(
            model_name='client',
            name='hsa_state',
            field=models.CharField(blank=True, null=True, max_length=255),
        ),
        migrations.AddField(
            model_name='client',
            name='student_loan_assistance_program',
            field=models.NullBooleanField(verbose_name='Assistance Program', help_text='Does your employer offer a loan repayment assistance program?'),
        ),
        migrations.AddField(
            model_name='client',
            name='student_loan_graduate_looking',
            field=models.NullBooleanField(verbose_name='Graduate', help_text='Are you a graduate looking to refinance your student loans?'),
        ),
        migrations.AddField(
            model_name='client',
            name='student_loan_parent_looking',
            field=models.NullBooleanField(verbose_name='Parent', help_text='Are you a parent looking to refinance Parent Plus loans?'),
        ),
    ]
