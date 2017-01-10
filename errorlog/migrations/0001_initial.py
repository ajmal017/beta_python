# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ErrorLog',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('source', models.IntegerField(choices=[(1, 'WebApp'), (2, 'Backend'), (3, 'FrontEnd')])),
                ('header', models.CharField(max_length=100)),
                ('message', models.TextField()),
                ('url', models.URLField()),
                ('details', jsonfield.fields.JSONField(blank=True, null=True)),
                ('version', models.CharField(max_length=100, blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='JiraTicket',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('ticket', models.URLField(blank=True, null=True)),
                ('header', models.CharField(max_length=100)),
                ('message', models.TextField()),
                ('task', models.CharField(max_length=100)),
            ],
        ),
        migrations.AlterIndexTogether(
            name='jiraticket',
            index_together=set([('header', 'message')]),
        ),
        migrations.AddField(
            model_name='errorlog',
            name='jira_ticket',
            field=models.ForeignKey(to='errorlog.JiraTicket', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='errorlog',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True, blank=True, related_name='logged_ui_errors'),
        ),
    ]
