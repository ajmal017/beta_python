# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators

def create_plans(apps, schema_editor):
    PricingPlan = apps.get_model("main", "PricingPlan")
    Firm = apps.get_model("main", "Firm")
    db_alias = schema_editor.connection.alias
    for firm in Firm.objects.using(db_alias).all():
        PricingPlan.objects.create(firm=firm)


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0043_riskprofilequestion_figure'),
        ('main', '0087_auto_20161220_1443'),
    ]

    operations = [
        migrations.CreateModel(
            name='PricingPlan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('bps', models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0)])),
                ('fixed', models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0)])),
                ('system_bps', models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0)])),
                ('system_fixed', models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0)])),
                ('firm', models.OneToOneField(to='main.Firm', related_name='pricing_plan')),
            ],
        ),
        migrations.CreateModel(
            name='PricingPlanAdvisor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('bps', models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0)])),
                ('fixed', models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0)])),
                ('parent', models.ForeignKey(to='main.PricingPlan', related_name='advisor_overrides')),
                ('person', models.OneToOneField(to='main.Advisor', related_name='pricing_plan')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PricingPlanClient',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('bps', models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0)])),
                ('fixed', models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0)])),
                ('parent', models.ForeignKey(to='main.PricingPlan', related_name='client_overrides')),
                ('person', models.OneToOneField(to='client.Client', related_name='pricing_plan')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RunPython(create_plans),
    ]
