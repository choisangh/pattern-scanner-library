"""Patterns representing head-and-shoulders structures."""

import pandas as pd
from sklearn.linear_model import LinearRegression
from ..core.abstract import AbstractPattern
from ..core.util import get_crosspt


class ReverseHeadAndShoulders(AbstractPattern):
    """Bullish reversal pattern with inverted head and shoulders."""
    def __init__(self, zigzag_df: pd.DataFrame, candle_df: pd.DataFrame):
        self.name = self.__class__.__name__
        self.start_price = 'high'
        self.second_price = self.get_second_price()
        self.pattern_type = 0
        self.point_num = 7
        self.zigzag_df = zigzag_df
        self.candle_df = candle_df

    def check_point_condition(self, point_value_list: list):
        p = point_value_list
        return (p[0] > p[2]) & (p[1] < p[2]) & (p[2] >= p[4]) & (p[1] > p[3]) & (p[3] < p[5]) & (p[3] < p[4]) & (p[5] < p[4])

    def check_time_condition(self, window: pd.DataFrame):
        return (window.iloc[2].name - window.iloc[0].name) < (window.iloc[4].name - window.iloc[2].name)

    def check_auxiliary_line_condition(self, p: pd.DataFrame, window: pd.DataFrame):
        neck = pd.DataFrame([[window.iloc[2].name, p[2]], [window.iloc[4].name, p[4]]])
        line_fitter = LinearRegression()
        line_fitter.fit(neck[[0]], neck[[1]])
        start_point_neck = line_fitter.predict([[window.index[0]]])
        return p[0] > start_point_neck[0][0]


class HeadAndShoulders(AbstractPattern):
    """Bearish reversal pattern with head and shoulders."""
    def __init__(self, zigzag_df: pd.DataFrame, candle_df: pd.DataFrame):
        self.name = self.__class__.__name__
        self.start_price = 'low'
        self.second_price = self.get_second_price()
        self.pattern_type = 0
        self.point_num = 7
        self.zigzag_df = zigzag_df
        self.candle_df = candle_df

    def check_point_condition(self, point_value_list: list):
        p = point_value_list
        return (p[0] < p[2]) & (p[1] > p[2]) & (p[2] <= p[4]) & (p[1] < p[3]) & (p[3] > p[5]) & (p[3] > p[4]) & (p[5] > p[4])

    def check_time_condition(self, window: pd.DataFrame):
        return (window.iloc[2].name - window.iloc[0].name) < (window.iloc[4].name - window.iloc[2].name)

    def check_auxiliary_line_condition(self, p: pd.DataFrame, window: pd.DataFrame):
        neck = pd.DataFrame([[window.iloc[2].name, p[2]], [window.iloc[4].name, p[4]]])
        line_fitter = LinearRegression()
        line_fitter.fit(neck[[0]], neck[[1]])
        start_point_neck = line_fitter.predict([[window.index[0]]])
        return p[0] < start_point_neck[0][0]

