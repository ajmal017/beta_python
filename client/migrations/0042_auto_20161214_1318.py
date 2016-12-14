# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0041_auto_20161212_1808'),
    ]

    operations = [
        migrations.CreateModel(
            name='JointAccountConfirmationModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_confirmed', models.DateTimeField(blank=True, null=True)),
                ('token', models.CharField(max_length=64)),
            ],
        ),
        migrations.AlterField(
            model_name='accounttyperiskprofilegroup',
            name='account_type',
            field=models.IntegerField(unique=True, choices=[(0, 'Personal Account'), (1, 'Joint Account'), (2, 'Trust Account'), (24, 'Investment Club Account'), (25, 'Partnership/Limited partnership Account'), (26, 'Sole Proprietor Account'), (27, 'Limited Liability Company Account'), (28, 'Association Account'), (29, 'Non-corporate organization Account'), (30, 'Pension Account'), (5, '401K Account'), (38, '401A Account'), (6, 'Roth 401K Account'), (7, 'Individual Retirement Account (IRA)'), (8, 'Roth IRA'), (9, 'SEP IRA'), (10, '403K Account'), (11, 'SIMPLE IRA Account (Savings Incentive Match Plans for Employees)'), (12, 'SARSEP Account (Salary Reduction Simplified Employee Pension)'), (13, 'Payroll Deduction IRA Account'), (14, 'Profit-Sharing Account'), (16, 'Money Purchase Account'), (17, 'Employee Stock Ownership Account (ESOP)'), (18, 'Governmental Account'), (19, '457 Account'), (20, '409A Nonqualified Deferred Compensation Account'), (21, '403B Account'), (31, 'Health Savings Account'), (32, '529 college savings plans Account'), (33, 'Coverdell Educational Savings Account (ESA) Account'), (34, 'UGMA/UTMA Account'), (35, 'Guardianship of the Estate Account'), (36, 'Custodial Account'), (37, 'Thrift Savings Account')]),
        ),
        migrations.AlterField(
            model_name='clientaccount',
            name='account_type',
            field=models.IntegerField(choices=[(0, 'Personal Account'), (1, 'Joint Account'), (2, 'Trust Account'), (24, 'Investment Club Account'), (25, 'Partnership/Limited partnership Account'), (26, 'Sole Proprietor Account'), (27, 'Limited Liability Company Account'), (28, 'Association Account'), (29, 'Non-corporate organization Account'), (30, 'Pension Account'), (5, '401K Account'), (38, '401A Account'), (6, 'Roth 401K Account'), (7, 'Individual Retirement Account (IRA)'), (8, 'Roth IRA'), (9, 'SEP IRA'), (10, '403K Account'), (11, 'SIMPLE IRA Account (Savings Incentive Match Plans for Employees)'), (12, 'SARSEP Account (Salary Reduction Simplified Employee Pension)'), (13, 'Payroll Deduction IRA Account'), (14, 'Profit-Sharing Account'), (16, 'Money Purchase Account'), (17, 'Employee Stock Ownership Account (ESOP)'), (18, 'Governmental Account'), (19, '457 Account'), (20, '409A Nonqualified Deferred Compensation Account'), (21, '403B Account'), (31, 'Health Savings Account'), (32, '529 college savings plans Account'), (33, 'Coverdell Educational Savings Account (ESA) Account'), (34, 'UGMA/UTMA Account'), (35, 'Guardianship of the Estate Account'), (36, 'Custodial Account'), (37, 'Thrift Savings Account')]),
        ),
        migrations.AddField(
            model_name='jointaccountconfirmationmodel',
            name='account',
            field=models.ForeignKey(related_name='joint_confirmation', to='client.ClientAccount'),
        ),
        migrations.AddField(
            model_name='jointaccountconfirmationmodel',
            name='cosignee',
            field=models.ForeignKey(related_name='cosignee_confirmation', to='client.Client'),
        ),
        migrations.AddField(
            model_name='jointaccountconfirmationmodel',
            name='primary_owner',
            field=models.ForeignKey(related_name='owner_confirmation', to='client.Client'),
        ),
    ]
