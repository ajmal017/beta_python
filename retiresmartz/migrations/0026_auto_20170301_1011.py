# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('retiresmartz', '0025_auto_20170228_0118'),
    ]

    operations = [
        migrations.AddField(
            model_name='retirementprojection',
            name='accounts_401a',
            field=jsonfield.fields.JSONField(help_text='List of annual accounts', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='retirementprojection',
            name='accounts_401k',
            field=jsonfield.fields.JSONField(help_text='List of annual accounts', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='retirementprojection',
            name='accounts_403b',
            field=jsonfield.fields.JSONField(help_text='List of annual accounts', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='retirementprojection',
            name='accounts_403k',
            field=jsonfield.fields.JSONField(help_text='List of annual accounts', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='retirementprojection',
            name='accounts_409a',
            field=jsonfield.fields.JSONField(help_text='List of annual accounts', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='retirementprojection',
            name='accounts_457',
            field=jsonfield.fields.JSONField(help_text='List of annual accounts', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='retirementprojection',
            name='accounts_esop',
            field=jsonfield.fields.JSONField(help_text='List of annual accounts', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='retirementprojection',
            name='accounts_gov',
            field=jsonfield.fields.JSONField(help_text='List of annual accounts', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='retirementprojection',
            name='accounts_ind_401k',
            field=jsonfield.fields.JSONField(help_text='List of annual accounts', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='retirementprojection',
            name='accounts_ind_roth_401k',
            field=jsonfield.fields.JSONField(help_text='List of annual accounts', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='retirementprojection',
            name='accounts_ira',
            field=jsonfield.fields.JSONField(help_text='List of annual accounts', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='retirementprojection',
            name='accounts_mon_purch',
            field=jsonfield.fields.JSONField(help_text='List of annual accounts', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='retirementprojection',
            name='accounts_pay_deduct_ira',
            field=jsonfield.fields.JSONField(help_text='List of annual accounts', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='retirementprojection',
            name='accounts_priv_457',
            field=jsonfield.fields.JSONField(help_text='List of annual accounts', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='retirementprojection',
            name='accounts_prof_sharing',
            field=jsonfield.fields.JSONField(help_text='List of annual accounts', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='retirementprojection',
            name='accounts_qual_annuity',
            field=jsonfield.fields.JSONField(help_text='List of annual accounts', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='retirementprojection',
            name='accounts_qual_np',
            field=jsonfield.fields.JSONField(help_text='List of annual accounts', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='retirementprojection',
            name='accounts_qual_np_roth',
            field=jsonfield.fields.JSONField(help_text='List of annual accounts', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='retirementprojection',
            name='accounts_roth_401k',
            field=jsonfield.fields.JSONField(help_text='List of annual accounts', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='retirementprojection',
            name='accounts_roth_ira',
            field=jsonfield.fields.JSONField(help_text='List of annual accounts', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='retirementprojection',
            name='accounts_sarsep_ira',
            field=jsonfield.fields.JSONField(help_text='List of annual accounts', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='retirementprojection',
            name='accounts_sep_ira',
            field=jsonfield.fields.JSONField(help_text='List of annual accounts', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='retirementprojection',
            name='accounts_simple_ira',
            field=jsonfield.fields.JSONField(help_text='List of annual accounts', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='retirementprojection',
            name='accounts_tax_def_annuity',
            field=jsonfield.fields.JSONField(help_text='List of annual accounts', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='retirementprojection',
            name='part_accounts_401a',
            field=jsonfield.fields.JSONField(help_text='List of annual accounts', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='retirementprojection',
            name='part_accounts_401k',
            field=jsonfield.fields.JSONField(help_text='List of annual accounts', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='retirementprojection',
            name='part_accounts_403b',
            field=jsonfield.fields.JSONField(help_text='List of annual accounts', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='retirementprojection',
            name='part_accounts_403k',
            field=jsonfield.fields.JSONField(help_text='List of annual accounts', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='retirementprojection',
            name='part_accounts_409a',
            field=jsonfield.fields.JSONField(help_text='List of annual accounts', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='retirementprojection',
            name='part_accounts_457',
            field=jsonfield.fields.JSONField(help_text='List of annual accounts', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='retirementprojection',
            name='part_accounts_esop',
            field=jsonfield.fields.JSONField(help_text='List of annual accounts', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='retirementprojection',
            name='part_accounts_gov',
            field=jsonfield.fields.JSONField(help_text='List of annual accounts', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='retirementprojection',
            name='part_accounts_ind_401k',
            field=jsonfield.fields.JSONField(help_text='List of annual accounts', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='retirementprojection',
            name='part_accounts_ind_roth_401k',
            field=jsonfield.fields.JSONField(help_text='List of annual accounts', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='retirementprojection',
            name='part_accounts_ira',
            field=jsonfield.fields.JSONField(help_text='List of annual accounts', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='retirementprojection',
            name='part_accounts_mon_purch',
            field=jsonfield.fields.JSONField(help_text='List of annual accounts', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='retirementprojection',
            name='part_accounts_pay_deduct_ira',
            field=jsonfield.fields.JSONField(help_text='List of annual accounts', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='retirementprojection',
            name='part_accounts_priv_457',
            field=jsonfield.fields.JSONField(help_text='List of annual accounts', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='retirementprojection',
            name='part_accounts_prof_sharing',
            field=jsonfield.fields.JSONField(help_text='List of annual accounts', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='retirementprojection',
            name='part_accounts_qual_annuity',
            field=jsonfield.fields.JSONField(help_text='List of annual accounts', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='retirementprojection',
            name='part_accounts_qual_np',
            field=jsonfield.fields.JSONField(help_text='List of annual accounts', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='retirementprojection',
            name='part_accounts_qual_np_roth',
            field=jsonfield.fields.JSONField(help_text='List of annual accounts', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='retirementprojection',
            name='part_accounts_roth_401k',
            field=jsonfield.fields.JSONField(help_text='List of annual accounts', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='retirementprojection',
            name='part_accounts_roth_ira',
            field=jsonfield.fields.JSONField(help_text='List of annual accounts', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='retirementprojection',
            name='part_accounts_sarsep_ira',
            field=jsonfield.fields.JSONField(help_text='List of annual accounts', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='retirementprojection',
            name='part_accounts_sep_ira',
            field=jsonfield.fields.JSONField(help_text='List of annual accounts', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='retirementprojection',
            name='part_accounts_simple_ira',
            field=jsonfield.fields.JSONField(help_text='List of annual accounts', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='retirementprojection',
            name='part_accounts_tax_def_annuity',
            field=jsonfield.fields.JSONField(help_text='List of annual accounts', blank=True, null=True),
        ),
    ]
