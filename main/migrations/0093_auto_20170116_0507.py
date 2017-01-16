# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0092_auto_20161229_1358'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExecutionFill',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('execution', models.OneToOneField(to='main.Execution', related_name='execution_fill')),
            ],
        ),
        migrations.CreateModel(
            name='Fill',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('volume', models.FloatField(help_text='Will be negative for a sell.')),
                ('price', models.FloatField(help_text='Price for the fill.')),
                ('executed', models.DateTimeField(help_text='The time the trade was executed.')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('Price', models.FloatField()),
                ('Exchange', models.CharField(max_length=128, default='Auto')),
                ('TrailingLimitAmount', models.FloatField(default=0)),
                ('AllOrNone', models.IntegerField(default=0)),
                ('TrailingStopAmount', models.FloatField(default=0)),
                ('Type', models.IntegerField(choices=[(0, 'Market'), (1, 'Limit')], default=1)),
                ('Quantity', models.IntegerField()),
                ('SecurityId', models.IntegerField()),
                ('Symbol', models.CharField(max_length=128, default='Auto')),
                ('Side', models.IntegerField(choices=[(0, 'Buy'), (1, 'Sell')])),
                ('TimeInForce', models.IntegerField(choices=[(0, 'Day'), (1, 'GoodTillCancel'), (2, 'AtTheOpening'), (3, 'ImmediateOrCancel'), (4, 'FillOrKill'), (5, 'GoodTillCrossing'), (6, 'GoodTillDate')], default=6)),
                ('StopPrice', models.FloatField(default=0)),
                ('ExpireDate', models.IntegerField()),
                ('created', models.DateTimeField(db_index=True, auto_now_add=True)),
                ('Order_Id', models.IntegerField(default=-1)),
                ('Status', models.CharField(choices=[('New', 'New'), ('Sent', 'Sent'), ('PartiallyFilled', 'PartiallyFilled'), ('Filled', 'Filled'), ('DoneForDay', 'DoneForDay'), ('Canceled', 'Canceled'), ('Replaced', 'Replaced'), ('PendingCancel', 'PendingCancel'), ('Stopped', 'Stopped'), ('Rejected', 'Rejected'), ('Suspended', 'Suspended'), ('PendingNew', 'PendingNew'), ('Calculated', 'Calculated'), ('Expired', 'Expired'), ('AcceptedForBidding', 'AcceptedForBidding'), ('PendingReplace', 'PendingReplace'), ('Error', 'Error'), ('Archived', 'Archived')], max_length=128, db_index=True, default='New')),
                ('FillPrice', models.FloatField(default=0)),
                ('FillQuantity', models.IntegerField(default=0)),
                ('Description', models.CharField(max_length=128)),
                ('Broker', models.CharField(max_length=128)),
                ('fill_info', models.IntegerField(choices=[(0, 'FILLED'), (1, 'PARTIALY_FILLED'), (2, 'UNFILLED')], default=2)),
                ('ticker', models.ForeignKey(to='main.Ticker', on_delete=django.db.models.deletion.PROTECT, related_name='Order')),
            ],
        ),
        migrations.RemoveField(
            model_name='apexfill',
            name='etna_order',
        ),
        migrations.RemoveField(
            model_name='executionapexfill',
            name='apex_fill',
        ),
        migrations.RemoveField(
            model_name='executionapexfill',
            name='execution',
        ),
        migrations.RemoveField(
            model_name='orderetna',
            name='ticker',
        ),
        migrations.RemoveField(
            model_name='marketorderrequestapex',
            name='etna_order',
        ),
        migrations.AlterField(
            model_name='activitylogevent',
            name='id',
            field=models.IntegerField(choices=[(0, 'PLACE_MARKET_ORDER'), (1, 'CANCEL_MARKET_ORDER'), (2, 'ARCHIVE_GOAL_REQUESTED'), (3, 'ARCHIVE_GOAL'), (4, 'REACTIVATE_GOAL'), (5, 'APPROVE_SELECTED_SETTINGS'), (6, 'REVERT_SELECTED_SETTINGS'), (7, 'SET_SELECTED_SETTINGS'), (8, 'UPDATE_SELECTED_SETTINGS'), (9, 'GOAL_WITHDRAWAL'), (10, 'GOAL_DEPOSIT'), (11, 'GOAL_BALANCE_CALCULATED'), (12, 'GOAL_WITHDRAWAL_EXECUTED'), (13, 'GOAL_DEPOSIT_EXECUTED'), (14, 'GOAL_DIVIDEND_DISTRIBUTION'), (15, 'GOAL_FEE_LEVIED'), (16, 'GOAL_REBALANCE_EXECUTED'), (17, 'GOAL_TRANSFER_EXECUTED'), (18, 'GOAL_ORDER_DISTRIBUTION'), (19, 'RETIRESMARTZ_PROTECTIVE_MOVE'), (20, 'RETIRESMARTZ_DYNAMIC_MOVE'), (21, 'RETIRESMARTZ_SPENDABLE_INCOME_UP_CONTRIB_DOWN'), (22, 'RETIRESMARTZ_SPENDABLE_INCOME_DOWN_CONTRIB_UP'), (23, 'RETIRESMARTZ_RETIREMENT_AGE_ADJUSTED'), (24, 'RETIRESMARTZ_IS_A_SMOKER'), (25, 'RETIRESMARTZ_IS_NOT_A_SMOKER'), (26, 'RETIRESMARTZ_EXERCISE_ONLY'), (27, 'RETIRESMARTZ_WEIGHT_AND_HEIGHT_ONLY'), (28, 'RETIRESMARTZ_COMBINATION_WELLBEING_ENTRIES'), (29, 'RETIRESMARTZ_ALL_WELLBEING_ENTRIES'), (30, 'RETIRESMARTZ_ON_TRACK_NOW'), (31, 'RETIRESMARTZ_OFF_TRACK_NOW'), (32, 'RETIRESMARTZ_CONTRIB_UP_SPENDING_DOWN'), (33, 'RETIRESMARTZ_DRINKS_MORE_THAN_ONE'), (34, 'RETIRESMARTZ_DRINKS_ONE_OR_LESS'), (50, 'ALLOCATION_CHANGED'), (51, 'TAX_LOSS_HARVESTED'), (52, 'STATEMENTS_GENERATED'), (53, 'TAX_FORMS_GENERATED'), (54, 'DOCUMENTS_GENERATED'), (55, 'OTHERS_GENERATED')], primary_key=True, serialize=False),
        ),
        migrations.DeleteModel(
            name='ApexFill',
        ),
        migrations.DeleteModel(
            name='ExecutionApexFill',
        ),
        migrations.DeleteModel(
            name='OrderETNA',
        ),
        migrations.AddField(
            model_name='fill',
            name='order',
            field=models.ForeignKey(to='main.Order', related_name='fills', default=None),
        ),
        migrations.AddField(
            model_name='executionfill',
            name='fill',
            field=models.ForeignKey(to='main.Fill', related_name='execution_fill'),
        ),
        migrations.AddField(
            model_name='marketorderrequestapex',
            name='order',
            field=models.ForeignKey(to='main.Order', related_name='morsAPEX', default=None),
        ),
    ]
