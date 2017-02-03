from datetime import date, datetime
from ujson import loads
from unittest import mock, skip
from unittest.mock import MagicMock
from dateutil.relativedelta import relativedelta
from django.utils.timezone import now
from rest_framework import status
from rest_framework.test import APITestCase
from common.constants import GROUP_SUPPORT_STAFF
from main.models import InvestmentType, GoalSetting, GoalMetricGroup, GoalMetric
from main.tests.fixture import Fixture1
from retiresmartz.models import RetirementPlan
from .factories import AssetClassFactory, ContentTypeFactory, GroupFactory, \
    RetirementPlanFactory, TickerFactory, RetirementAdviceFactory
from .factories import ExternalAssetFactory, MarkowitzScaleFactory, MarketIndexFactory, \
    PortfolioSetFactory, RetirementStatementOfAdviceFactory, EmailInviteFactory, ClientFactory
from django.conf import settings

mocked_now = datetime(2016, 1, 1)


class PlaidTests(APITestCase):
    def setUp(self):
        self.support_group = GroupFactory.create(name=GROUP_SUPPORT_STAFF)
        self.betasmartz_client = ClientFactory.create()

    def test_create_access_token(self):
        url = '/api/v1/plaid/create-access-token'
        data = {
            "public_token": 'test,chase,connected',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(user=self.betasmartz_client.user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('success'), True)

    def test_get_accounts(self):
        url = '/api/v1/plaid/get-accounts'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(user=self.betasmartz_client.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
