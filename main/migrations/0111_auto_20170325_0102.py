# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0110_auto_20170324_0854'),
    ]

    operations = [
        migrations.AddField(
            model_name='firmdata',
            name='advisor_support_email',
            field=models.EmailField(verbose_name='Client Support Email', max_length=254, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='firmdata',
            name='advisor_support_phone',
            field=models.CharField(verbose_name='Advisor Support Phone', max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='firmdata',
            name='advisor_support_workhours',
            field=models.TextField(verbose_name='Advisor Support Workhours', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='firmdata',
            name='client_support_email',
            field=models.EmailField(verbose_name='Client Support Email', max_length=254, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='firmdata',
            name='client_support_phone',
            field=models.CharField(verbose_name='Client Support Phone', max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='firmdata',
            name='client_support_workhours',
            field=models.TextField(verbose_name='Client Support Workhours', null=True, blank=True),
        ),
    ]
