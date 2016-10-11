from collections import defaultdict
from datetime import timedelta
import pandas as pd
from portfolios.providers.dummy_models import AssetClassMock, \
    AssetFeatureValueMock, InstrumentsFactory, MarkowitzScaleMock, \
    PortfolioSetMock, InvestmentCycleObservationFactory
from portfolios.returns import get_prices
from .abstract import DataProviderAbstract


class DataProviderBacktester(DataProviderAbstract):
    def __init__(self, sliding_window_length):
        self.sliding_window_length = sliding_window_length
        self.cache = None
        self.markowitz_scale = None
        self.tickers = list()
        self.benchmark_marketweight_matrix = pd.read_csv('capitalization_mock.csv',
                                                         index_col='Date',
                                                         infer_datetime_format=True,
                                                         parse_dates=True)
        self.portfolio_sets = [PortfolioSetMock(name='portfolio_set1',
                                                asset_classes=[AssetClassMock("equity"),
                                                               AssetClassMock("fixed Income")],
                                                views=None
                                                )]
        self.asset_feature_values = [AssetFeatureValueMock(name='featureName',
                                                           feature=None,
                                                           tickers=['EEM', 'EEMV', 'EFA'])]
        self.tickers = InstrumentsFactory.create_tickers()
        self.dates = InstrumentsFactory.get_dates()
        self.__current_date = self.sliding_window_length
        self.time_constrained_tickers = []
        self.investment_cycles = InvestmentCycleObservationFactory.create_cycles()

    def move_date_forward(self):
        # this function is only used in backtesting
        self.cache = None
        success = False
        if len(self.dates) > self.__current_date + 1:
            self.__current_date += 1
            success = True
        else:
            print("cannot move date forward")
        return success

    def get_current_date(self):
        date = self.dates[self.__current_date]
        return pd.Timestamp(date).to_datetime()

    def get_start_date(self):
        date = self.dates[self.__current_date - self.sliding_window_length]
        return pd.Timestamp(date).to_datetime()

    def get_fund_price_latest(self, ticker):
        prices = get_prices(ticker, self.get_start_date(), self.get_current_date())
        prices = prices.irow(-1)
        return prices

    def get_features(self, ticker):
        return ticker.features

    def get_asset_class_to_portfolio_set(self):
        ac_ps = defaultdict(list)
        for ps in self.portfolio_sets:
            for ac in ps.asset_classes:
                ac_ps[ac.id].append(ps.id)
        return ac_ps

    def get_tickers(self):
        self.time_constrained_tickers = []
        for ticker in self.tickers:
            date_range = (self.get_current_date() - timedelta(days=self.sliding_window_length),
                          self.get_current_date())

            ticker = InstrumentsFactory.create_ticker(ticker=ticker.symbol,
                                                      daily_prices=ticker.daily_prices.filter(date__range=date_range),
                                                      benchmark_id=ticker.benchmark.symbol,
                                                      benchmark_daily_prices=
                                                      ticker.benchmark.daily_prices.filter(date__range=date_range)
                                                      )
            self.time_constrained_tickers.append(ticker)
        return self.time_constrained_tickers

    def get_ticker(self, tid):
        ticker = None
        for t in self.time_constrained_tickers:
            if t.id == tid:
                ticker = t
                break
        return ticker

    def get_market_weight(self, content_type_id, content_object_id):
        # provide market cap for a given benchmark at a given date (latest available) - use get_current_date
        mp = self.benchmark_marketweight_matrix.ix[:self.get_current_date(), content_type_id]
        if mp.shape[0] > 0:
            mp = mp.irow(-1)
        else:
            mp = None
        return None if mp is None else mp

    def get_portfolio_sets_ids(self):
        return [val.id for val in self.portfolio_sets]

    def get_asset_feature_values_ids(self):
        return [val.id for val in self.asset_feature_values]

    def get_goals(self):
        return

    def get_markowitz_scale(self):
        if self.markowitz_scale is None:
            self.set_markowitz_scale(date=self.get_current_date(), min=-1, max=1, a=1, b=2, c=3)
        return self.markowitz_scale

    def set_markowitz_scale(self, date, mn, mx, a, b, c):
        self.markowitz_scale = MarkowitzScaleMock(date, mn, mx, a, b, c)

    def get_instrument_cache(self):
        return self.cache

    def set_instrument_cache(self, data):
        self.cache = data

    def get_investment_cycles(self):
        return self.investment_cycles

    def get_last_cycle_start(self):
        pass

    def get_cycle_obs(self, begin_date):
        pass

    def get_probs_df(self, begin_date):
        pass

