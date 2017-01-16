# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0094_firm_site_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='firmdata',
            name='afsl_asic',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='AFSL/ASIC number'),
        ),
        migrations.AlterField(
            model_name='firmdata',
            name='afsl_asic_document',
            field=models.FileField(blank=True, null=True, verbose_name='AFSL/ASIC doc.', upload_to=''),
        ),
        migrations.AlterField(
            model_name='firmdata',
            name='australian_business_number',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='ABN'),
        ),
        migrations.AlterField(
            model_name='firmdata',
            name='fax_num',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=16, null=True),
        ),
        migrations.AlterField(
            model_name='firmdata',
            name='fee_bank_account_branch_name',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Branch name'),
        ),
        migrations.AlterField(
            model_name='firmdata',
            name='fee_bank_account_bsb_number',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='BSB number'),
        ),
        migrations.AlterField(
            model_name='firmdata',
            name='fee_bank_account_holder_name',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Account holder'),
        ),
        migrations.AlterField(
            model_name='firmdata',
            name='fee_bank_account_name',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='firmdata',
            name='fee_bank_account_number',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Account number'),
        ),
        migrations.AlterField(
            model_name='firmdata',
            name='mobile_phone_num',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=16, null=True),
        ),
        migrations.AlterField(
            model_name='firmdata',
            name='office_address',
            field=models.ForeignKey(blank=True, to='address.Address', null=True, related_name='+'),
        ),
    ]
