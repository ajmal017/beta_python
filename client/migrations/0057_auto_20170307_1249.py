# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0056_auto_20170224_1510'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailinvite',
            name='salutation',
            field=models.CharField(choices=[('Mr.', 'Mr.'), ('Mrs.', 'Mrs.'), ('Ms.', 'Ms.'), ('Dr.', 'Dr.')], default='Mr.', max_length=10),
        ),
        migrations.AddField(
            model_name='emailinvite',
            name='suffix',
            field=models.CharField(choices=[('Sr.', 'Sr.'), ('Jr.', 'Jr.'), ('I', 'I'), ('II', 'II'), ('III', 'III'), ('IV', 'IV'), ('V', 'V')], null=True, blank=True, max_length=10),
        ),
    ]
