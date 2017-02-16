# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('retiresmartz', '0020_retirementplan_date_of_estimate'),
    ]

    operations = [
        migrations.CreateModel(
            name='RetirementProjection',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('income_actual_monthly', jsonfield.fields.JSONField(null=True, blank=True, help_text="List of monthly actual income")),
                ('income_desired_monthly', jsonfield.fields.JSONField(null=True, blank=True, help_text="List of monthly desired income")),
                ('taxable_assets_monthly', jsonfield.fields.JSONField(null=True, blank=True, help_text="List of monthly taxable assets")),
                ('nontaxable_assets_monthly', jsonfield.fields.JSONField(null=True, blank=True, help_text="List of monthly nontaxable assets")),
                ('proj_balance_at_retire_in_todays', models.FloatField(null=True, default=0, help_text="Projected balance at retirement in today's money")),
                ('proj_inc_actual_at_retire_in_todays', models.FloatField(null=True, default=0, help_text="Projected monthly income actual at retirement in today's money")),
                ('proj_inc_desired_at_retire_in_todays', models.FloatField(null=True, default=0, help_text="Projected monthly income desired at retirement in today's money")),
                ('savings_end_date_as_age', models.FloatField(null=True, default=0, help_text='Projected age post retirement when taxable assets first deplete to zero')),
                ('current_percent_soc_sec', models.FloatField(null=True, default=0, help_text='Current percentage of monthly income represented by payments made towards social security')),
                ('current_percent_medicare', models.FloatField(null=True, default=0, help_text='Current percentage of monthly income represented by payments made towards medicare')),
                ('current_percent_fed_tax', models.FloatField(null=True, default=0, help_text='Current percentage of monthly income represented by payments made towards federal taxes')),
                ('current_percent_state_tax', models.FloatField(null=True, default=0, help_text='Current percentage of monthly income represented by payments made towards state taxes')),
                ('non_taxable_inc', jsonfield.fields.JSONField(blank=True, null=True, help_text='List of monthly non taxable monthly income received')),
                ('tot_taxable_dist', jsonfield.fields.JSONField(blank=True, null=True, help_text='List of monthly total taxable distributions received')),
                ('annuity_payments', jsonfield.fields.JSONField(blank=True, null=True, help_text='List of monthly annuity payments received')),
                ('pension_payments', jsonfield.fields.JSONField(blank=True, null=True, help_text='List of monthly pension payments received')),
                ('ret_working_inc', jsonfield.fields.JSONField(blank=True, null=True, help_text='List of monthly retirement working payments received')),
                ('soc_sec_benefit', jsonfield.fields.JSONField(blank=True, null=True, help_text='List of monthly social security benefit payments received')),
                ('taxable_accounts', jsonfield.fields.JSONField(blank=True, null=True, help_text='List of monthly taxable accounts')),
                ('non_taxable_accounts', jsonfield.fields.JSONField(blank=True, null=True, help_text='List of monthly nontaxable accounts')),
                ('reverse_mort', models.BooleanField(default=False, null=False, help_text="Whether user has a reverse mortgage")),
                ('house_value', models.FloatField(default=0, null=True, help_text="Current value of house")),
                ('house_value_at_retire_in_todays', models.FloatField(default=0, null=True, help_text="Future value of house in todays")),
                ('reverse_mort_pymnt_at_retire_in_todays', models.FloatField(default=0, null=True, help_text="Future value of monthly reverse mortgage payment in todays")),
                ('part_income_actual_monthly', jsonfield.fields.JSONField(null=True, blank=True, help_text="List of monthly actual income")),
                ('part_income_desired_monthly', jsonfield.fields.JSONField(null=True, blank=True, help_text="List of monthly desired income")),
                ('part_taxable_assets_monthly', jsonfield.fields.JSONField(null=True, blank=True, help_text="List of monthly taxable assets")),
                ('part_nontaxable_assets_monthly', jsonfield.fields.JSONField(null=True, blank=True, help_text="List of monthly nontaxable assets")),
                ('part_proj_balance_at_retire_in_todays', models.FloatField(null=True, default=0, help_text="Projected balance at retirement in today's money")),
                ('part_proj_inc_actual_at_retire_in_todays', models.FloatField(null=True, default=0, help_text="Projected monthly income actual at retirement in today's money")),
                ('part_proj_inc_desired_at_retire_in_todays', models.FloatField(null=True, default=0, help_text="Projected monthly income desired at retirement in today's money")),
                ('part_savings_end_date_as_age', models.FloatField(null=True, default=0, help_text='Projected age post retirement when taxable assets first deplete to zero')),
                ('part_current_percent_soc_sec', models.FloatField(null=True, default=0, help_text='Current percentage of monthly income represented by payments made towards social security')),
                ('part_current_percent_medicare', models.FloatField(null=True, default=0, help_text='Current percentage of monthly income represented by payments made towards medicare')),
                ('part_current_percent_fed_tax', models.FloatField(null=True, default=0, help_text='Current percentage of monthly income represented by payments made towards federal taxes')),
                ('part_current_percent_state_tax', models.FloatField(null=True, default=0, help_text='Current percentage of monthly income represented by payments made towards state taxes')),
                ('part_non_taxable_inc', jsonfield.fields.JSONField(blank=True, null=True, help_text='List of monthly non taxable monthly income received')),
                ('part_tot_taxable_dist', jsonfield.fields.JSONField(blank=True, null=True, help_text='List of monthly total taxable distributions received')),
                ('part_annuity_payments', jsonfield.fields.JSONField(blank=True, null=True, help_text='List of monthly annuity payments received')),
                ('part_pension_payments', jsonfield.fields.JSONField(blank=True, null=True, help_text='List of monthly pension payments received')),
                ('part_ret_working_inc', jsonfield.fields.JSONField(blank=True, null=True, help_text='List of monthly retirement working payments received')),
                ('part_soc_sec_benefit', jsonfield.fields.JSONField(blank=True, null=True, help_text='List of monthly social security benefit payments received')),
                ('part_taxable_accounts', jsonfield.fields.JSONField(blank=True, null=True, help_text='List of monthly taxable accounts')),
                ('part_non_taxable_accounts', jsonfield.fields.JSONField(blank=True, null=True, help_text='List of monthly nontaxable accounts')),
                ('part_reverse_mort', models.BooleanField(default=False, null=False, help_text="Whether user has a reverse mortgage")),
                ('part_house_value', models.FloatField(default=0, null=True, help_text="Current value of house")),
                ('part_house_value_at_retire_in_todays', models.FloatField(default=0, null=True, help_text="Future value of house in todays")),
                ('part_reverse_mort_pymnt_at_retire_in_todays', models.FloatField(default=0, null=True, help_text="Future value of monthly reverse mortgage payment in todays")),
                ('plan', models.OneToOneField(to='retiresmartz.RetirementPlan', null=True, related_name='projection')),
            ],
        ),
    ]
