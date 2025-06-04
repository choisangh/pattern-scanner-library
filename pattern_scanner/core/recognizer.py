"""Utilities for detecting candlestick patterns on time series data."""

import pandas as pd
import numpy as np
from scipy.signal import argrelextrema
from .abstract import AbstractPattern



class PatternRecognizer:
    """Attach pattern detectors to candlestick data."""
    def __init__(self, window_size: int,
                 timestamp: pd.Series,
                 open_price: pd.Series,
                 high_price: pd.Series,
                 low_price: pd.Series,
                 close_price: pd.Series,
                 volume: pd.Series):
        """Preprocess data and instantiate pattern classes."""
        self.candle_df = self.make_candle_df(timestamp, open_price, high_price, low_price, close_price, volume)
        pattern_class_list = AbstractPattern.__subclasses__()
        self.zigzag_df = self.make_zigzag(window_size)
        for pattern_class in pattern_class_list:
            self.add_attribute(f'{pattern_class.__name__}', pattern_class(self.zigzag_df, self.candle_df))

    def add_attribute(self, name, value):
        """Attach a pattern instance to this recognizer."""
        setattr(self.__class__, name, value)

    @staticmethod
    def get_pattern_list():
        """Print available pattern class names."""
        print([f'{pattern_class.__name__}' for pattern_class in AbstractPattern.__subclasses__()])

    @staticmethod
    def make_candle_df(timestamp: pd.Series, openprice: pd.Series,
                       highprice: pd.Series, lowprice: pd.Series,
                       closeprice: pd.Series, volume: pd.Series):
        """Combine series into a single DataFrame used for scanning."""
        candle_df = pd.concat([timestamp, openprice,
                               highprice, lowprice,
                               closeprice, volume], axis=1)
        candle_df.columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
        return candle_df

    @staticmethod
    def processing_max_min(prices: pd.DataFrame, order: int) -> pd.DataFrame:  # 최대 최소값 찾기 (꼭지점)
        """Return local extrema used to create zigzag points."""
        window_range = 1
        prices['t'] = pd.to_datetime(prices['timestamp'])
        prices = prices.sort_values('timestamp')
        prices = prices.set_index('timestamp')

        local_max = argrelextrema(prices.high.values, np.greater_equal, order=order)[0]  # 로컬 최대값 찾기 (양옆보다 큼)
        local_min = argrelextrema(prices.low.values, np.less_equal, order=order)[0]  # 로컬 최소값 찾기 (양옆보다 작음)
        price_local_max_dt = []
        for i in local_max:
            if (i >= window_range) and (i < len(prices) - window_range):
                price_local_max_dt.append(prices.iloc[i - window_range:i + window_range]['high'].idxmax())
        price_local_min_dt = []
        for i in local_min:
            if (i >= window_range) and (i < len(prices) - window_range):
                price_local_min_dt.append(prices.iloc[i - window_range:i + window_range]['low'].idxmin())
        maxima = pd.DataFrame(prices.loc[price_local_max_dt], columns=['high'])
        minima = pd.DataFrame(prices.loc[price_local_min_dt], columns=['low'])
        max_min = pd.concat([maxima, minima]).sort_index()
        max_min.index.name = 'date'
        max_min = max_min.reset_index()
        max_min = max_min[~max_min.date.duplicated()]
        p = prices.reset_index()
        max_min['day_num'] = p[p['timestamp'].isin(max_min.date)].index.values
        max_min = max_min.set_index('day_num')[['high', 'low', 'date']]

        return max_min

    @staticmethod
    def processing__zigzag(max_min: pd.DataFrame) -> pd.DataFrame:
        """Filter alternating highs and lows to form zigzag segments."""
        del_list = []
        for i in range(max_min.shape[0] - 1):
            if (np.isnan(max_min.iloc[i, 0]) is False) and (np.isnan(max_min.iloc[i + 1, 0]) is False):
                if max_min.iloc[i, 0] < max_min.iloc[i + 1, 0]:
                    del_list.append(max_min.iloc[i].name)
                else:
                    del_list.append(max_min.iloc[i + 1].name)

            elif (np.isnan(max_min.iloc[i, 1]) is False) and (np.isnan(max_min.iloc[i + 1, 1]) is False):
                if max_min.iloc[i, 1] > max_min.iloc[i + 1, 1]:
                    del_list.append(max_min.iloc[i].name)
                else:
                    del_list.append(max_min.iloc[i + 1].name)
            else:
                pass
        max_min = max_min.drop(del_list, axis=0)
        del_list = []
        for i in range(max_min.shape[0] - 1):
            if (np.isnan(max_min.iloc[i, 0]) is False) and (np.isnan(max_min.iloc[i + 1, 0]) is False):
                if max_min.iloc[i, 0] < max_min.iloc[i + 1, 0]:
                    del_list.append(max_min.iloc[i].name)
                else:
                    del_list.append(max_min.iloc[i + 1].name)

            elif (np.isnan(max_min.iloc[i, 1]) is False) and (np.isnan(max_min.iloc[i + 1, 1]) is False):
                if max_min.iloc[i, 1] > max_min.iloc[i + 1, 1]:
                    del_list.append(max_min.iloc[i].name)
                else:
                    del_list.append(max_min.iloc[i + 1].name)
            else:
                pass
        zigzag_df = max_min.drop(del_list, axis=0)
        return zigzag_df

    def make_zigzag(self, window_size: int):
        """Generate zigzag points based on a detection window."""
        max_min = self.processing_max_min(self.candle_df, window_size)
        zigzag = self.processing__zigzag(max_min)
        return zigzag
