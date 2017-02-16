# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('retiresmartz', '0021_retirementprojection'),
    ]

    operations = [
        migrations.AlterField(
            model_name='retirementprojection',
            name='annuity_payments',
            field=jsonfield.fields.JSONField(blank=True, help_text='List of ammual annuity payments received', null=True),
        ),
        migrations.AlterField(
            model_name='retirementprojection',
            name='non_taxable_accounts',
            field=jsonfield.fields.JSONField(blank=True, help_text='List of annual nontaxable accounts', null=True),
        ),
        migrations.AlterField(
            model_name='retirementprojection',
            name='non_taxable_inc',
            field=jsonfield.fields.JSONField(blank=True, help_text='List of annual non taxable monthly income received', null=True),
        ),
        migrations.AlterField(
            model_name='retirementprojection',
            name='part_annuity_payments',
            field=jsonfield.fields.JSONField(blank=True, help_text='List of annual annuity payments received', null=True),
        ),
        migrations.AlterField(
            model_name='retirementprojection',
            name='part_non_taxable_accounts',
            field=jsonfield.fields.JSONField(blank=True, help_text='List of annual nontaxable accounts', null=True),
        ),
        migrations.AlterField(
            model_name='retirementprojection',
            name='part_non_taxable_inc',
            field=jsonfield.fields.JSONField(blank=True, help_text='List of annual non taxable monthly income received', null=True),
        ),
        migrations.AlterField(
            model_name='retirementprojection',
            name='part_pension_payments',
            field=jsonfield.fields.JSONField(blank=True, help_text='List of annual pension payments received', null=True),
        ),
        migrations.AlterField(
            model_name='retirementprojection',
            name='part_ret_working_inc',
            field=jsonfield.fields.JSONField(blank=True, help_text='List of annual retirement working payments received', null=True),
        ),
        migrations.AlterField(
            model_name='retirementprojection',
            name='part_soc_sec_benefit',
            field=jsonfield.fields.JSONField(blank=True, help_text='List of annual social security benefit payments received', null=True),
        ),
        migrations.AlterField(
            model_name='retirementprojection',
            name='part_taxable_accounts',
            field=jsonfield.fields.JSONField(blank=True, help_text='List of annual taxable accounts', null=True),
        ),
        migrations.AlterField(
            model_name='retirementprojection',
            name='part_tot_taxable_dist',
            field=jsonfield.fields.JSONField(blank=True, help_text='List of annual total taxable distributions received', null=True),
        ),
        migrations.AlterField(
            model_name='retirementprojection',
            name='pension_payments',
            field=jsonfield.fields.JSONField(blank=True, help_text='List of annual pension payments received', null=True),
        ),
        migrations.AlterField(
            model_name='retirementprojection',
            name='ret_working_inc',
            field=jsonfield.fields.JSONField(blank=True, help_text='List of annual retirement working payments received', null=True),
        ),
        migrations.AlterField(
            model_name='retirementprojection',
            name='soc_sec_benefit',
            field=jsonfield.fields.JSONField(blank=True, help_text='List of annual social security benefit payments received', null=True),
        ),
        migrations.AlterField(
            model_name='retirementprojection',
            name='taxable_accounts',
            field=jsonfield.fields.JSONField(blank=True, help_text='List of annual taxable accounts', null=True),
        ),
        migrations.AlterField(
            model_name='retirementprojection',
            name='tot_taxable_dist',
            field=jsonfield.fields.JSONField(blank=True, help_text='List of annual total taxable distributions received', null=True),
        ),
    ]
