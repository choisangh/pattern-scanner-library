"""Triangle pattern implementations."""

import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from ..core.abstract import AbstractPattern


class AscendingTriangle(AbstractPattern):
    """Continuation pattern with rising lows and flat highs."""
    def __init__(self, zigzag_df: pd.DataFrame, candle_df: pd.DataFrame):
        self.name = self.__class__.__name__
        self.start_price = 'high'
        self.second_price = self.get_second_price()
        self.pattern_type = 1
        self.point_num = 5
        self.zigzag_df = zigzag_df
        self.candle_df = candle_df

    def check_point_condition(self, point_value_list: list):
        p = point_value_list
        scaler = MinMaxScaler()
        scaled_p = scaler.fit_transform([[p[0]], [p[1]], [p[2]], [p[3]]])
        condition1 = (p[2] < p[4]) & (p[1] < p[3])
        condition2 = (scaled_p[0][0] > 0.9) & (scaled_p[2][0] > 0.9)
        return condition1 & condition2

    def check_time_condition(self, window: pd.DataFrame):
        return True

    def check_auxiliary_line_condition(self, p: pd.DataFrame, window: pd.DataFrame):
        return True


class DescendingTriangle(AbstractPattern):
    """Continuation pattern with falling highs and flat lows."""
    def __init__(self, zigzag_df: pd.DataFrame, candle_df: pd.DataFrame):
        self.name = self.__class__.__name__
        self.start_price = 'low'
        self.second_price = self.get_second_price()
        self.pattern_type = 1
        self.point_num = 5
        self.zigzag_df = zigzag_df
        self.candle_df = candle_df

    def check_point_condition(self, point_value_list: list):
        p = point_value_list
        scaler = MinMaxScaler()
        scaled_p = scaler.fit_transform([[p[0]], [p[1]], [p[2]], [p[3]]])
        condition1 = (p[2] > p[4]) & (p[1] > p[3])
        condition2 = (scaled_p[0][0] < 0.1) & (scaled_p[2][0] < 0.1)
        return condition1 & condition2

    def check_time_condition(self, window: pd.DataFrame):
        return True

    def check_auxiliary_line_condition(self, p: pd.DataFrame, window: pd.DataFrame):
        return True


class BullishTriangle(AbstractPattern):
    """Bullish breakout from converging trend lines."""
    def __init__(self, zigzag_df: pd.DataFrame, candle_df: pd.DataFrame):
        self.name = self.__class__.__name__
        self.start_price = 'high'
        self.second_price = self.get_second_price()
        self.pattern_type = 1
        self.point_num = 5
        self.zigzag_df = zigzag_df
        self.candle_df = candle_df

    def check_point_condition(self, point_value_list: list):
        p = point_value_list
        scaler = MinMaxScaler()
        scaled_p = scaler.fit_transform([[p[0]], [p[1]], [p[2]], [p[3]]])
        condition1 = (p[2] < p[4]) & (p[1] < p[3]) & (p[0] > p[2])
        condition2 = (scaled_p[0][0] > 0.9) & (scaled_p[2][0] < 0.9)
        return condition1 & condition2

    def check_time_condition(self, window: pd.DataFrame):
        return True

    def check_auxiliary_line_condition(self, p: pd.DataFrame, window: pd.DataFrame):
        return True


class BearishTriangle(AbstractPattern):
    """Bearish breakout from converging trend lines."""
    def __init__(self, zigzag_df: pd.DataFrame, candle_df: pd.DataFrame):
        self.name = self.__class__.__name__
        self.start_price = 'low'
        self.second_price = self.get_second_price()
        self.pattern_type = 1
        self.point_num = 5
        self.zigzag_df = zigzag_df
        self.candle_df = candle_df

    def check_point_condition(self, point_value_list: list):
        p = point_value_list
        scaler = MinMaxScaler()
        scaled_p = scaler.fit_transform([[p[0]], [p[1]], [p[2]], [p[3]]])
        condition1 = (p[2] > p[4]) & (p[1] > p[3])
        condition2 = (scaled_p[0][0] < 0.1) & (scaled_p[2][0] > 0.1)
        return condition1 & condition2

    def check_time_condition(self, window: pd.DataFrame):
        return True

    def check_auxiliary_line_condition(self, p: pd.DataFrame, window: pd.DataFrame):
        return True

