# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0094_auto_20170112_0632'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlaidUser',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('access_token', models.CharField(max_length=255)),
                ('user', models.OneToOneField(related_name='plaid_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
