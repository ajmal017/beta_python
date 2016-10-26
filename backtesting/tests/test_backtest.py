from unittest.case import skip

import pandas as pd
from django.test import TestCase
from backtesting.backtester import TestSetup, Backtester
from statsmodels.stats.correlation_tools import cov_nearest

from main.models import AssetClass, GoalMetric, InvestmentType, \
    MarketIndex, MarkowitzScale, Portfolio, PortfolioItem, Region, \
    Ticker
from main.tests.fixture import Fixture1
from portfolios.calculation import build_instruments, calculate_portfolio, \
    calculate_portfolios, get_instruments
from portfolios.providers.execution.django import ExecutionProviderDjango
from portfolios.providers.data.django import DataProviderDjango
from main.tests.fixture import Fixture1
from main.management.commands.rebalance import rebalance


class BaseTest(TestCase):
    def test_backtest(self):
        setup = TestSetup()
        self.create_goal()
        setup.create_goal(self.goal)
        setup.data_provider.move_date_forward()

        backtester = Backtester()

        print("backtesting " + str(setup.data_provider.get_current_date()))
        build_instruments(setup.data_provider)

        portfolios_stats = calculate_portfolios(setting=setup.goal.selected_settings,
                                                data_provider=setup.data_provider,
                                                execution_provider=setup.execution_provider)
        portfolio_stats = calculate_portfolio(settings=setup.goal.selected_settings,
                                              data_provider=setup.data_provider,
                                              execution_provider=setup.execution_provider)

        requests = rebalance(idata=get_instruments(setup.data_provider),
                             goal=setup.goal,
                             data_provider=setup.data_provider,
                             execution_provider=setup.execution_provider)

        performance = backtester.calculate_performance(execution_provider=setup.execution_provider)

    def create_goal(self):
        self.goal = Fixture1.goal1()
