"""Pattern implementations for double top and bottom formations."""

import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from ..core.abstract import AbstractPattern


class DoubleBottom(AbstractPattern):
    """Detect the bullish double bottom reversal pattern."""
    def __init__(self, zigzag_df: pd.DataFrame, candle_df: pd.DataFrame):
        self.name = self.__class__.__name__
        self.start_price = 'high'
        self.second_price = self.get_second_price()
        self.pattern_type = 0
        self.point_num = 5
        self.zigzag_df = zigzag_df
        self.candle_df = candle_df

    def check_point_condition(self, point_value_list: list):
        p = point_value_list
        scaler = MinMaxScaler()
        scaled_p = scaler.fit_transform([[p[0]], [p[1]], [p[2]], [p[3]], [p[4]]])
        return (scaled_p[1][0] < 0.06) & (scaled_p[3][0] < 0.06)

    def check_time_condition(self, window: pd.DataFrame):
        condition1 = (window.iloc[2].name - window.iloc[0].name) * 1.5 > (window.iloc[4].name - window.iloc[2].name)
        condition2 = (window.iloc[2].name - window.iloc[0].name) < (window.iloc[4].name - window.iloc[2].name) * 1.5
        return condition1 & condition2

    def check_auxiliary_line_condition(self, p: pd.DataFrame, window: pd.DataFrame):
        return True


class DoubleTop(AbstractPattern):
    """Detect the bearish double top reversal pattern."""
    def __init__(self, zigzag_df: pd.DataFrame, candle_df: pd.DataFrame):
        self.name = self.__class__.__name__
        self.start_price = 'low'
        self.second_price = self.get_second_price()
        self.pattern_type = 0
        self.point_num = 5
        self.zigzag_df = zigzag_df
        self.candle_df = candle_df

    def check_point_condition(self, point_value_list: list):
        p = point_value_list
        scaler = MinMaxScaler()
        scaled_p = scaler.fit_transform([[p[0]], [p[1]], [p[2]], [p[3]], [p[4]]])
        return (scaled_p[1][0] > 0.94) & (scaled_p[3][0] > 0.94)

    def check_time_condition(self, window: pd.DataFrame):
        condition1 = (window.iloc[2].name - window.iloc[0].name) * 1.5 > (window.iloc[4].name - window.iloc[2].name)
        condition2 = (window.iloc[2].name - window.iloc[0].name) < (window.iloc[4].name - window.iloc[2].name) * 1.5
        return condition1 & condition2

    def check_auxiliary_line_condition(self, p: pd.DataFrame, window: pd.DataFrame):
        return True

