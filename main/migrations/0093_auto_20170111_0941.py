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
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('execution', models.OneToOneField(related_name='execution_fill', to='main.Execution')),
            ],
        ),
        migrations.CreateModel(
            name='Fill',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('volume', models.FloatField(help_text='Will be negative for a sell.')),
                ('price', models.FloatField(help_text='Price for the fill.')),
                ('executed', models.DateTimeField(help_text='The time the trade was executed.')),
            ],
        ),
        migrations.CreateModel(
            name='MarketOrderRequestAPEX',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('market_order_request', models.ForeignKey(related_name='morsAPEX', to='main.MarketOrderRequest')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('Price', models.FloatField()),
                ('Exchange', models.CharField(default='Auto', max_length=128)),
                ('TrailingLimitAmount', models.FloatField(default=0)),
                ('AllOrNone', models.IntegerField(default=0)),
                ('TrailingStopAmount', models.FloatField(default=0)),
                ('Type', models.IntegerField(default=1, choices=[(0, 'Market'), (1, 'Limit')])),
                ('Quantity', models.IntegerField()),
                ('SecurityId', models.IntegerField()),
                ('Symbol', models.CharField(default='Auto', max_length=128)),
                ('Side', models.IntegerField(choices=[(0, 'Buy'), (1, 'Sell')])),
                ('TimeInForce', models.IntegerField(default=6, choices=[(0, 'Day'), (1, 'GoodTillCancel'), (2, 'AtTheOpening'), (3, 'ImmediateOrCancel'), (4, 'FillOrKill'), (5, 'GoodTillCrossing'), (6, 'GoodTillDate')])),
                ('StopPrice', models.FloatField(default=0)),
                ('ExpireDate', models.IntegerField()),
                ('created', models.DateTimeField(db_index=True, auto_now_add=True)),
                ('Order_Id', models.IntegerField(default=-1)),
                ('Status', models.CharField(db_index=True, choices=[('New', 'New'), ('Sent', 'Sent'), ('PartiallyFilled', 'PartiallyFilled'), ('Filled', 'Filled'), ('DoneForDay', 'DoneForDay'), ('Canceled', 'Canceled'), ('Replaced', 'Replaced'), ('PendingCancel', 'PendingCancel'), ('Stopped', 'Stopped'), ('Rejected', 'Rejected'), ('Suspended', 'Suspended'), ('PendingNew', 'PendingNew'), ('Calculated', 'Calculated'), ('Expired', 'Expired'), ('AcceptedForBidding', 'AcceptedForBidding'), ('PendingReplace', 'PendingReplace'), ('Error', 'Error'), ('Archived', 'Archived')], default='New', max_length=128)),
                ('FillPrice', models.FloatField(default=0)),
                ('FillQuantity', models.IntegerField(default=0)),
                ('Description', models.CharField(max_length=128)),
                ('Broker', models.CharField(max_length=128)),
                ('fill_info', models.IntegerField(default=2, choices=[(0, 'FILLED'), (1, 'PARTIALY_FILLED'), (2, 'UNFILLED')])),
                ('ticker', models.ForeignKey(related_name='Order', on_delete=django.db.models.deletion.PROTECT, to='main.Ticker')),
            ],
        ),
        migrations.AddField(
            model_name='executiondistribution',
            name='execution_request',
            field=models.ForeignKey(blank=True, related_name='execution_distributions', to='main.ExecutionRequest', null=True),
        ),
        migrations.AlterField(
            model_name='activitylogevent',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False, choices=[(0, 'PLACE_MARKET_ORDER'), (1, 'CANCEL_MARKET_ORDER'), (2, 'ARCHIVE_GOAL_REQUESTED'), (3, 'ARCHIVE_GOAL'), (4, 'REACTIVATE_GOAL'), (5, 'APPROVE_SELECTED_SETTINGS'), (6, 'REVERT_SELECTED_SETTINGS'), (7, 'SET_SELECTED_SETTINGS'), (8, 'UPDATE_SELECTED_SETTINGS'), (9, 'GOAL_WITHDRAWAL'), (10, 'GOAL_DEPOSIT'), (11, 'GOAL_BALANCE_CALCULATED'), (12, 'GOAL_WITHDRAWAL_EXECUTED'), (13, 'GOAL_DEPOSIT_EXECUTED'), (14, 'GOAL_DIVIDEND_DISTRIBUTION'), (15, 'GOAL_FEE_LEVIED'), (16, 'GOAL_REBALANCE_EXECUTED'), (17, 'GOAL_TRANSFER_EXECUTED'), (18, 'GOAL_ORDER_DISTRIBUTION'), (19, 'RETIRESMARTZ_PROTECTIVE_MOVE'), (20, 'RETIRESMARTZ_DYNAMIC_MOVE'), (21, 'RETIRESMARTZ_SPENDABLE_INCOME_UP_CONTRIB_DOWN'), (22, 'RETIRESMARTZ_SPENDABLE_INCOME_DOWN_CONTRIB_UP'), (23, 'RETIRESMARTZ_RETIREMENT_AGE_ADJUSTED'), (24, 'RETIRESMARTZ_IS_A_SMOKER'), (25, 'RETIRESMARTZ_IS_NOT_A_SMOKER'), (26, 'RETIRESMARTZ_EXERCISE_ONLY'), (27, 'RETIRESMARTZ_WEIGHT_AND_HEIGHT_ONLY'), (28, 'RETIRESMARTZ_COMBINATION_WELLBEING_ENTRIES'), (29, 'RETIRESMARTZ_ALL_WELLBEING_ENTRIES'), (30, 'RETIRESMARTZ_ON_TRACK_NOW'), (31, 'RETIRESMARTZ_OFF_TRACK_NOW'), (32, 'RETIRESMARTZ_CONTRIB_UP_SPENDING_DOWN'), (33, 'RETIRESMARTZ_DRINKS_MORE_THAN_ONE'), (34, 'RETIRESMARTZ_DRINKS_ONE_OR_LESS'), (50, 'ALLOCATION_CHANGED'), (51, 'TAX_LOSS_HARVESTED'), (52, 'STATEMENTS_GENERATED'), (53, 'TAX_FORMS_GENERATED'), (54, 'DOCUMENTS_GENERATED'), (55, 'OTHERS_GENERATED')]),
        ),
        migrations.AddField(
            model_name='marketorderrequestapex',
            name='order',
            field=models.ForeignKey(default=None, related_name='morsAPEX', to='main.Order'),
        ),
        migrations.AddField(
            model_name='marketorderrequestapex',
            name='ticker',
            field=models.ForeignKey(related_name='morsAPEX', on_delete=django.db.models.deletion.PROTECT, to='main.Ticker'),
        ),
        migrations.AddField(
            model_name='fill',
            name='order',
            field=models.ForeignKey(default=None, related_name='fills', to='main.Order'),
        ),
        migrations.AddField(
            model_name='executionfill',
            name='fill',
            field=models.ForeignKey(related_name='execution_fill', to='main.Fill'),
        ),
        migrations.AlterUniqueTogether(
            name='marketorderrequestapex',
            unique_together=set([('ticker', 'market_order_request')]),
        ),
    ]
