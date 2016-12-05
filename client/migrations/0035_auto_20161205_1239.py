# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0034_auto_20161203_0331'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='industry_sector',
            field=models.CharField(choices=[('NAICS 11', 'Agriculture, Forestry, Fishing and Hunting'), ('NAICS 21', 'Mining, Quarrying, and Oil and Gas Extraction'), ('NAICS 23', 'Construction'), ('NAICS 31-33', 'Manufacturing'), ('NAICS 42', 'Wholesale Trade'), ('NAICS 44-45', 'Retail Trade '), ('NAICS 48-49', 'Transportation and Warehousing'), ('NAICS 22', 'Utilities'), ('NAICS 51', 'Information'), ('NAICS 52', 'Finance and Insurance '), ('NAICS 53', 'Real Estate and Rental and Leasing '), ('NAICS 531', 'Real Estate '), ('NAICS 54', 'Professional, Scientific, and Technical Services '), ('NAICS 55', 'Management of Companies and Enterprises '), ('NAICS 56', 'Administrative and Support and Waste Management and Remediation Services'), ('NAICS 61', 'Educational Services'), ('NAICS 62', 'Health Care and Social Assistance'), ('NAICS 71', 'Arts, Entertainment, and Recreation'), ('NAICS 72', 'Accommodation and Food Services '), ('NAICS 81', 'Other Services')], max_length=10, blank=True, null=True),
        ),
    ]
