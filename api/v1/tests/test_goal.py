from decimal import Decimal

from pinax.eventlog.models import Log
from rest_framework import status
from rest_framework.test import APITestCase

from common.constants import GROUP_SUPPORT_STAFF
from main.event import Event
from main.models import ActivityLog, ActivityLogEvent, EventMemo, \
    MarketOrderRequest
from main.tests.fixture import Fixture1
from .factories import GroupFactory, GoalFactory, ClientAccountFactory, \
    GoalSettingFactory
from api.v1.goals.serializers import GoalSettingSerializer
import ujson


class GoalTests(APITestCase):
    def setUp(self):
        self.support_group = GroupFactory(name=GROUP_SUPPORT_STAFF)

    def tearDown(self):
        self.client.logout()

    def test_get_list(self):
        goal = Fixture1.goal1()
        goal.approve_selected()
        url = '/api/v1/goals'
        self.client.force_authenticate(user=Fixture1.client1().user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        # Make sure for the list endpoint, selected settings is an object, but active and approved are null or integer.
        self.assertEqual(response.data[0]['active_settings'], None)
        self.assertEqual(response.data[0]['approved_settings'], response.data[0]['selected_settings']['id'])

    def test_get_detail(self):
        goal = Fixture1.goal1()
        url = '/api/v1/goals/{}'.format(goal.id)
        goal.approve_selected()
        self.client.force_authenticate(user=Fixture1.client1().user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], Fixture1.goal1().id)
        # Make sure for the detail endpoint, selected settings is an object, but active and approved are null or integer.
        self.assertEqual(response.data['active_settings'], None)
        self.assertEqual(response.data['approved_settings'], response.data['selected_settings']['id'])

    def test_get_no_activity(self):
        url = '/api/v1/goals/{}/activity'.format(Fixture1.goal1().id)
        self.client.force_authenticate(user=Fixture1.client1().user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_get_all_activity(self):
        # First add some transactions, balances and eventlogs, and make sure the ActivityLogs are set.
        Fixture1.settings_event1()
        Fixture1.transaction_event1()
        Fixture1.populate_balance1()  # 2 Activity lines
        # We also need to activate the activity logging for the desired event types.
        ActivityLogEvent.get(Event.APPROVE_SELECTED_SETTINGS)
        ActivityLogEvent.get(Event.GOAL_BALANCE_CALCULATED)
        ActivityLogEvent.get(Event.GOAL_DEPOSIT_EXECUTED)

        url = '/api/v1/goals/{}/activity'.format(Fixture1.goal1().id)
        self.client.force_authenticate(user=Fixture1.client1().user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)
        # Note the Goal not included in response as it is in request.
        self.assertEqual(response.data[0], {'time': 946684800,
                                            'type': ActivityLogEvent.get(Event.APPROVE_SELECTED_SETTINGS).activity_log.id})  # Setting change approval
        self.assertEqual(response.data[1], {'balance': 0.0,
                                            'time': 978220800,
                                            'type': ActivityLogEvent.get(Event.GOAL_BALANCE_CALCULATED).activity_log.id})  # Balance
        # Deposit. Note inclusion of amount, as we're looking at it from the goal perspective.
        self.assertEqual(response.data[2], {'amount': 3000.0,
                                            'data': [3000.0],
                                            'time': 978307200,
                                            'type': ActivityLogEvent.get(Event.GOAL_DEPOSIT_EXECUTED).activity_log.id})
        self.assertEqual(response.data[3], {'balance': 3000.0,
                                            'time': 978307200,
                                            'type': ActivityLogEvent.get(Event.GOAL_BALANCE_CALCULATED).activity_log.id})  # Balance

    def test_event_memo(self):
        '''
        Tests event memos and assigning multiple events to one activity log item.
        :return:
        '''
        # Add a public settings event with a memo
        se = Fixture1.settings_event1()
        EventMemo.objects.create(event=se, comment='A memo for e1', staff=False)
        # Add a staff settings event with a memo
        se2 = Fixture1.settings_event2()
        EventMemo.objects.create(event=se2, comment='A memo for e2', staff=True)
        # Add a transaction event without a memo
        Fixture1.transaction_event1()
        # We also need to activate the activity logging for the desired event types.
        # We add selected and update to the same une to test that too
        al = ActivityLog.objects.create(name="Settings Funk", format_str='Settings messed with')
        ActivityLogEvent.objects.create(id=Event.APPROVE_SELECTED_SETTINGS.value, activity_log=al)
        ActivityLogEvent.objects.create(id=Event.UPDATE_SELECTED_SETTINGS.value, activity_log=al)
        ActivityLogEvent.get(Event.GOAL_DEPOSIT_EXECUTED)

        url = '/api/v1/goals/{}/activity'.format(Fixture1.goal1().id)
        # Log in as a client and make sure I see the public settings event, and the transaction, not the staff entry.
        self.client.force_authenticate(user=Fixture1.client1().user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.data[0]['memos'], ['A memo for e1'])
        self.assertFalse('memos' in response.data[1])
        self.assertFalse('memos' in response.data[2])

        # Log in as the advisor and make sure I see all three events.
        self.client.force_authenticate(user=Fixture1.advisor1().user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.data[0]['memos'], ['A memo for e1'])
        self.assertEqual(response.data[1]['memos'], ['A memo for e2'])
        self.assertFalse('memos' in response.data[2])

    def test_performance_history_empty(self):
        url = '/api/v1/goals/{}/performance-history'.format(Fixture1.goal1().id)
        self.client.force_authenticate(user=Fixture1.client1().user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_performance_history(self):
        prices = (
            (Fixture1.fund1(), '20160101', 10),
            (Fixture1.fund1(), '20160102', 10.5),
            (Fixture1.fund1(), '20160103', 10.6),
            (Fixture1.fund1(), '20160104', 10.3),
            (Fixture1.fund1(), '20160105', 10.1),
            (Fixture1.fund1(), '20160106', 9.9),
            (Fixture1.fund1(), '20160107', 10.5),
            (Fixture1.fund2(), '20160101', 50),
            (Fixture1.fund2(), '20160102', 51),
            (Fixture1.fund2(), '20160103', 53),
            (Fixture1.fund2(), '20160104', 53.5),
            (Fixture1.fund2(), '20160105', 51),
            (Fixture1.fund2(), '20160106', 52),
            (Fixture1.fund2(), '20160107', 51.5),
        )
        Fixture1.set_prices(prices)

        order_details = (
            (Fixture1.personal_account1(), MarketOrderRequest.State.COMPLETE),
            (Fixture1.personal_account1(), MarketOrderRequest.State.COMPLETE),
            (Fixture1.personal_account1(), MarketOrderRequest.State.COMPLETE),
            (Fixture1.personal_account1(), MarketOrderRequest.State.COMPLETE),
            (Fixture1.personal_account1(), MarketOrderRequest.State.COMPLETE),
            (Fixture1.personal_account1(), MarketOrderRequest.State.COMPLETE),
        )
        orders = Fixture1.add_orders(order_details)

        execution_details = (
            (Fixture1.fund1(), orders[0], 3, 10.51, -75, '20160102'),
            (Fixture1.fund1(), orders[0], 4, 10.515, -75.05, '20160102'),
            (Fixture1.fund1(), orders[1], -1, 10.29, 10, '20160104'),
            (Fixture1.fund2(), orders[2], 2, 53.49, -110, '20160104'),
            (Fixture1.fund2(), orders[2], 8, 53.5, -430, '20160104'),
            (Fixture1.fund1(), orders[3], -3, 10.05, 30, '20160105'),
            (Fixture1.fund2(), orders[4], -3, 50.05, 145, '20160105'),
            (Fixture1.fund2(), orders[4], -2, 50.04, 98, '20160105'),
            (Fixture1.fund2(), orders[5], -5, 52, 255, '20160106'),
        )
        executions = Fixture1.add_executions(execution_details)

        # We distribute the entire executions to one goal.
        distributions = (
            (executions[0], 3, Fixture1.goal1()),
            (executions[1], 4, Fixture1.goal1()),
            (executions[2], -1, Fixture1.goal1()),
            (executions[3], 2, Fixture1.goal1()),
            (executions[4], 8, Fixture1.goal1()),
            (executions[5], -3, Fixture1.goal1()),
            (executions[6], -3, Fixture1.goal1()),
            (executions[7], -2, Fixture1.goal1()),
            (executions[8], -5, Fixture1.goal1()),
        )
        Fixture1.add_execution_distributions(distributions)

        url = '/api/v1/goals/{}/performance-history'.format(Fixture1.goal1().id)
        self.client.force_authenticate(user=Fixture1.client1().user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0], (16802, 0))  # 20160102
        self.assertEqual(response.data[1], (16803, Decimal('0.009524')))
        self.assertEqual(response.data[2], (16804, Decimal('-0.028302')))
        self.assertEqual(response.data[3], (16805, Decimal('-0.043901')))
        self.assertEqual(response.data[4], (16806, Decimal('-0.019802')))
        self.assertEqual(response.data[5], (16807, Decimal('0.060606')))
        self.assertEqual(response.data[6], (16808, 0))

    def test_put_settings_no_memo(self):
        # Test PUT with no memo
        old_events = Log.objects.count()
        old_memos = EventMemo.objects.count()
        url = '/api/v1/goals/{}/selected-settings'.format(Fixture1.goal1().id)
        self.client.force_authenticate(user=Fixture1.client1().user)
        settings_changes = {"target": 1928355}
        response = self.client.put(url, settings_changes)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Make sure an event log was written
        self.assertEqual(old_events + 1, Log.objects.count())
        # Make sure no event memo was written
        self.assertEqual(old_memos, EventMemo.objects.count())

    def test_put_settings_with_memo_no_staff(self):
        # Test with a memo but no staff
        old_events = Log.objects.count()
        old_memos = EventMemo.objects.count()
        url = '/api/v1/goals/{}/selected-settings'.format(Fixture1.goal1().id)
        self.client.force_authenticate(user=Fixture1.client1().user)
        settings_changes = {
            "target": 1928355,
            "event_memo": "Changed the target because I took an arrow to the knee."
        }
        response = self.client.put(url, settings_changes)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Make sure an event log was written
        self.assertEqual(old_events + 1, Log.objects.count())
        # Make sure an event memo was written
        self.assertEqual(old_memos + 1, EventMemo.objects.count())
        # Make sure the memo was the text I passed, and the default for staff is false.
        memo = EventMemo.objects.order_by('-id')[0]
        self.assertFalse(memo.staff)
        self.assertEqual(memo.comment, settings_changes['event_memo'])

    def test_put_settings_with_memo_true_staff(self):
        # Test with a memo and true staff
        old_events = Log.objects.count()
        old_memos = EventMemo.objects.count()
        url = '/api/v1/goals/{}/selected-settings'.format(Fixture1.goal1().id)
        self.client.force_authenticate(user=Fixture1.client1().user)
        settings_changes = {
            "target": 1928355,
            "event_memo": "Changed the target because I took an arrow to the knee.",
            "event_memo_staff": True,
        }
        response = self.client.put(url, settings_changes)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Make sure an event log was written
        self.assertEqual(old_events + 1, Log.objects.count())
        # Make sure an event memo was written
        self.assertEqual(old_memos + 1, EventMemo.objects.count())
        # Make sure the memo was the text I passed, and staff is true.
        memo = EventMemo.objects.order_by('-id')[0]
        self.assertTrue(memo.staff)
        self.assertEqual(memo.comment, settings_changes['event_memo'])

    def test_post_settings_with_memo_false_staff(self):
        # Test POST with a memo and false staff
        old_events = Log.objects.count()
        old_memos = EventMemo.objects.count()
        url = '/api/v1/goals/{}/selected-settings'.format(Fixture1.goal1().id)
        self.client.force_authenticate(user=Fixture1.client1().user)
        new_settings = {
            "completion": "2016-01-01",
            "metric_group": {"metrics": []},
            "hedge_fx": False,
            "event_memo": "Replaced because the old one smelled.",
            "event_memo_staff": False,
        }
        response = self.client.post(url, new_settings)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Make sure an event log was written
        self.assertEqual(old_events + 1, Log.objects.count())
        # Make sure an event memo was written
        self.assertEqual(old_memos + 1, EventMemo.objects.count())
        # Make sure the memo was the text I passed, and staff is false.
        memo = EventMemo.objects.order_by('-id')[0]
        self.assertFalse(memo.staff)
        self.assertEqual(memo.comment, new_settings['event_memo'])

    def test_get_pending_transfers(self):
        # Populate an executed deposit and make sure no pending transfers are returned
        tx1 = Fixture1.transaction1()
        url = '/api/v1/goals/{}/pending-transfers'.format(Fixture1.goal1().id)
        self.client.force_authenticate(user=Fixture1.client1().user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

        # Populate 2 pending transfers (a deposit and withdrawal) and make sure they are both returned.
        tx2 = Fixture1.pending_deposit1()
        tx3 = Fixture1.pending_withdrawal1()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = [
            {
                "id": 3,
                "time": 946652400,
                "amount": -3500.0
            },
            {
                "id": 2,
                "time": 946648800,
                "amount": 4000.0
            }
        ]
        self.assertEqual(response.data, data)

    def test_recommended_risk_scores(self):
        """
        expects the years parameter for the span of risk scores
        """
        url = '/api/v1/goals/{}/recommended-risk-scores?years=9'.format(Fixture1.goal1().id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(user=Fixture1.client1().user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_calculate_all_portfolios(self):
        """
        expects the setting parameter to be a json dump
        of the goal settings to use for the portfolio calculation
        """
        account = ClientAccountFactory.create(primary_owner=Fixture1.client1())
        goal_settings = GoalSettingFactory.create()
        goal = GoalFactory.create(account=account, active_settings=goal_settings)
        # GoalSettingSerializer(goal_settings)
        settings_str = '%7B%22completion%22%3A%222026-01-07%22%2C%22hedge_fx%22%3Afalse%2C%22metric_group%22%3A%7B%22metrics%22%3A%5B%7B%22id%22%3A1107%2C%22type%22%3A1%2C%22comparison%22%3A1%2C%22rebalance_type%22%3A0%2C%22rebalance_thr%22%3A0.05%2C%22configured_val%22%3A0.5%2C%22measured_val%22%3Anull%2C%22feature%22%3Anull%7D%5D%7D%2C%22rebalance%22%3Atrue%2C%22recurring_transactions%22%3A%5B%7B%22amount%22%3A5%2C%22schedule%22%3A%22RRULE%3AFREQ%3DMONTHLY%3BBYMONTHDAY%3D6%22%2C%22begin_date%22%3A%222016-09-07%22%2C%22growth%22%3A0%7D%5D%2C%22target%22%3A80000%7D'
        print(ujson.load(settings_str))
        url = '/api/v1/goals/{}/calculate-all-portfolios?setting={}'.format(goal.id, settings_str)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(user=Fixture1.client1().user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
