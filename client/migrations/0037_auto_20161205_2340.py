# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0036_client_student_loan'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='industry_sector',
            field=models.CharField(blank=True, choices=[('NAICS 11', 'Agriculture, Forestry, Fishing and Hunting'), ('NAICS 21', 'Mining, Quarrying, and Oil and Gas Extraction'), ('NAICS 23', 'Construction'), ('NAICS 31-33', 'Manufacturing'), ('NAICS 42', 'Wholesale Trade'), ('NAICS 44-45', 'Retail Trade '), ('NAICS 48-49', 'Transportation and Warehousing'), ('NAICS 22', 'Utilities'), ('NAICS 51', 'Information'), ('NAICS 52', 'Finance and Insurance '), ('NAICS 53', 'Real Estate and Rental and Leasing '), ('NAICS 531', 'Real Estate '), ('NAICS 54', 'Professional, Scientific, and Technical Services '), ('NAICS 55', 'Management of Companies and Enterprises '), ('NAICS 56', 'Administrative and Support and Waste Management and Remediation Services'), ('NAICS 61', 'Educational Services'), ('NAICS 62', 'Health Care and Social Assistance'), ('NAICS 71', 'Arts, Entertainment, and Recreation'), ('NAICS 72', 'Accommodation and Food Services '), ('NAICS 81', 'Other Services')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='occupation',
            field=models.CharField(blank=True, choices=[('11-0000', 'Management'), ('13-0000', 'Business and Financial Operations'), ('15-0000', 'Computer and Mathematical'), ('17-0000', 'Architecture and Engineering'), ('19-0000', 'Life, Physical, and Social Science'), ('21-0000', 'Community and Social Services'), ('23-0000', 'Legal'), ('25-0000', 'Education, Training, and Library'), ('27-0000', 'Arts, Design, Entertainment, Sports, and Media'), ('29-0000', 'Healthcare Practitioners and Technical'), ('31-0000', 'Healthcare Support'), ('33-0000', 'Protective Service'), ('35-0000', 'Food Preparation and Serving Related'), ('37-0000', 'Building and Grounds Cleaning and Maintenance'), ('39-0000', 'Personal Care and Service'), ('41-0000', 'Sales and Related'), ('43-0000', 'Office and Administrative Support'), ('45-0000', 'Farming, Fishing, and Forestry'), ('47-0000', 'Construction and Extraction'), ('49-0000', 'Installation, Maintenance, and Repair'), ('51-0000', 'Production'), ('53-0000', 'Transportation and Material Moving'), ('55-0000', 'Military Specific')], max_length=20, null=True),
        ),
    ]
