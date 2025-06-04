"""Wedge pattern implementations."""

import pandas as pd
from sklearn.linear_model import LinearRegression
from ..core.abstract import AbstractPattern
from ..core.util import get_crosspt


class RisingWedge(AbstractPattern):
    """Bearish pattern formed by converging upward sloping trend lines."""
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
        return (p[0] < p[1]) & (p[1] < p[3]) & (p[1] > p[2]) & (p[2] < p[3]) & (p[3] > p[4]) & (p[4] > p[2]) & (p[2] > p[0]) & (p[4] > p[2])

    def check_time_condition(self, window: pd.DataFrame):
        return (window.iloc[2].name - window.iloc[0].name) > (window.iloc[4].name - window.iloc[2].name)

    def check_auxiliary_line_condition(self, p: pd.DataFrame, window: pd.DataFrame):
        cx, cy = get_crosspt(window.iloc[1].name, p[1], window.iloc[3].name, p[3], window.iloc[0].name, p[0], window.iloc[2].name, p[2])
        chart_length = window.iloc[-1].name - window.iloc[0].name
        triangle_length = cx - window.iloc[-1].name
        down_model = LinearRegression()
        down_line = pd.DataFrame([[window.iloc[0].name, p[0]], [window.iloc[2].name, p[2]]])
        down_model.fit(down_line[[0]], down_line[[1]])
        target = down_model.predict([[window.index[4]]])
        return (p[4] < target[0][0]) & (chart_length > triangle_length)


class FallingWedge(AbstractPattern):
    """Bullish pattern formed by converging downward sloping trend lines."""
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
        return (p[0] > p[1]) & (p[1] > p[3]) & (p[1] < p[2]) & (p[2] > p[3]) & (p[3] < p[4]) & (p[4] < p[2]) & (p[2] < p[0]) & (p[4] < p[2])

    def check_time_condition(self, window: pd.DataFrame):
        return (window.iloc[2].name - window.iloc[0].name) > (window.iloc[4].name - window.iloc[2].name)

    def check_auxiliary_line_condition(self, p: pd.DataFrame, window: pd.DataFrame):
        cx, cy = get_crosspt(window.iloc[1].name, p[1], window.iloc[3].name, p[3], window.iloc[0].name, p[0], window.iloc[2].name, p[2])
        chart_length = window.iloc[-1].name - window.iloc[0].name
        triangle_length = cx - window.iloc[-1].name
        upper_model = LinearRegression()
        upper_line = pd.DataFrame([[window.iloc[0].name, p[0]], [window.iloc[2].name, p[2]]])
        upper_model.fit(upper_line[[0]], upper_line[[1]])
        target = upper_model.predict([[window.index[4]]])
        return (p[4] > target[0][0]) & (chart_length > triangle_length)

