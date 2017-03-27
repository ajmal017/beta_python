# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0004_auto_20170125_0046'),
        ('client', '0057_auto_20170307_1249'),
    ]

    operations = [
        migrations.CreateModel(
            name='IBOnboard',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('account_number', models.CharField(blank=True, null=True, max_length=32)),
                ('country_of_birth', models.CharField(blank=True, help_text='Country of birth', null=True, max_length=250)),
                ('num_dependents', models.IntegerField(blank=True, help_text='Number of dependents', verbose_name='Number of dependents', null=True)),
                ('phone_type', models.CharField(blank=True, help_text='Phone Type', null=True, default='Home', choices=[('Work', 'Work'), ('Home', 'Home'), ('Fax', 'Fax'), ('Mobile', 'Mobile'), ('Mobile (work)', 'Mobile (work)'), ('Mobile (other)', 'Mobile (other)'), ('Business', 'Business'), ('Other (voice)', 'Other (voice)')], max_length=32)),
                ('identif_leg_citizenship', models.CharField(blank=True, help_text='Legal residence citizenship', verbose_name='Legal residence citizenship', null=True, max_length=250)),
                ('fin_info_tot_assets', models.IntegerField(blank=True, help_text='Total assets', default=5, null=True, verbose_name='Total Assets')),
                ('fin_info_liq_net_worth', models.IntegerField(blank=True, help_text='Liquid net worth', default=5, null=True, verbose_name='Liquid Net Worth')),
                ('fin_info_ann_net_inc', models.IntegerField(blank=True, help_text='Annual net income', default=5, null=True, verbose_name='Annual Net Income')),
                ('fin_info_net_worth', models.IntegerField(blank=True, help_text='Net worth', default=5, null=True, verbose_name='Net Worth')),
                ('asset_exp_0_knowledge', models.IntegerField(blank=True, help_text='STK trading knowledge', verbose_name='STK trading knowledge', null=True)),
                ('asset_exp_0_yrs', models.IntegerField(blank=True, help_text='STK trading experience', verbose_name='STK trading experience', null=True)),
                ('asset_exp_0_trds_per_yr', models.IntegerField(blank=True, help_text='STK trading frequency', verbose_name='STK trading frequency', null=True)),
                ('asset_exp_1_knowledge', models.IntegerField(blank=True, help_text='FUNDS trading knowledge', verbose_name='FUNDS trading knowledge', null=True)),
                ('asset_exp_1_yrs', models.IntegerField(blank=True, help_text='FUNDS trading experience', verbose_name='FUNDS trading experience', null=True)),
                ('asset_exp_1_trds_per_yr', models.IntegerField(blank=True, help_text='FUNDS trading frequency', verbose_name='Fund Trades Per Year', null=True)),
                ('reg_status_broker_deal', models.NullBooleanField(help_text='BROKERDEALER', verbose_name='BROKERDEALER')),
                ('reg_status_exch_memb', models.NullBooleanField(help_text='EXCHANGEMEMBERSHIP', verbose_name='EXCHANGEMEMBERSHIP')),
                ('reg_status_disp', models.NullBooleanField(help_text='DISPUTE', verbose_name='DISPUTE')),
                ('reg_status_investig', models.NullBooleanField(help_text='INVESTIGATION', verbose_name='Investigation')),
                ('reg_status_stk_cont', models.NullBooleanField(help_text='STKCONTROL')),
                ('tax_resid_0_tin_type', models.CharField(blank=True, help_text='Tax residency TIN type', verbose_name='Tax residency TIN type', null=True, default='SSN', choices=[('SSN', 'SSN'), ('EIN', 'EIN'), ('NonUS_NationalIID', 'NonUS_NationalIID')], max_length=250)),
                ('tax_resid_0_tin', models.CharField(blank=True, help_text='Tax residency TIN', verbose_name='Tax residency TIN', null=True, max_length=250)),
                ('doc_exec_ts', models.DateTimeField(auto_now_add=True, null=True)),
                ('doc_exec_login_ts', models.DateTimeField(auto_now_add=True, null=True)),
                ('doc_signed_by', models.CharField(blank=True, help_text='Document signed by', verbose_name='Document signed by', null=True, max_length=250)),
                ('salutation', models.CharField(help_text='Salutation', default='Mr.', choices=[('Mr.', 'Mr.'), ('Mrs.', 'Mrs.'), ('Ms.', 'Ms.'), ('Dr.', 'Dr.')], max_length=10)),
                ('suffix', models.CharField(blank=True, help_text='Suffix', choices=[('Sr.', 'Sr.'), ('Jr.', 'Jr.'), ('I', 'I'), ('II', 'II'), ('III', 'III'), ('IV', 'IV'), ('V', 'V')], max_length=10, null=True)),
                ('client', models.OneToOneField(blank=True, to='client.Client', null=True, related_name='ib_onboard')),
                ('employer_address', models.OneToOneField(blank=True, to='address.Address', null=True, related_name='ib_onboard_employer')),
                ('tax_address', models.OneToOneField(blank=True, to='address.Address', null=True, related_name='ib_onboard_tax')),
            ],
        ),
    ]
