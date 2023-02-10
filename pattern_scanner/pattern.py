from typing import Union

import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LinearRegression
from util import get_crosspt
from abstaract_pattern import AbstractPattern


class ReverseHeadAndShoulders(AbstractPattern):
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
        result = (p[0] > p[2]) & (p[1] < p[2]) & (p[2] >= p[4]) & (p[1] > p[3]) & (p[3] < p[5]) & (p[3] < p[4]) & (
                    p[5] < p[4])
        return result

    def check_time_condition(self, window: pd.DataFrame):
        result = (window.iloc[2].name - window.iloc[0].name) < (window.iloc[4].name - window.iloc[2].name)
        return result

    def check_auxiliary_line_condition(self, p: pd.DataFrame, window: pd.DataFrame):
        neck = pd.DataFrame([[window.iloc[2].name, p[2]], [window.iloc[4].name, p[4]]])
        line_fitter = LinearRegression()
        line_fitter.fit(neck[[0]], neck[[1]])
        start_point_neck = line_fitter.predict([[window.index[0]]])
        auxiliary_line_condition = (p[0] > start_point_neck[0][0])
        return auxiliary_line_condition


class HeadAndShoulders(AbstractPattern):
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
        result = (p[0] < p[2]) & (p[1] > p[2]) & (p[2] <= p[4]) & (p[1] < p[3]) & (p[3] > p[5]) & (p[3] > p[4]) & (
                    p[5] > p[4])
        return result

    def check_time_condition(self, window: pd.DataFrame):
        result = (window.iloc[2].name - window.iloc[0].name) < (window.iloc[4].name - window.iloc[2].name)
        return result

    def check_auxiliary_line_condition(self, p: pd.DataFrame, window: pd.DataFrame):
        neck = pd.DataFrame([[window.iloc[2].name, p[2]], [window.iloc[4].name, p[4]]])
        line_fitter = LinearRegression()
        line_fitter.fit(neck[[0]], neck[[1]])
        start_point_neck = line_fitter.predict([[window.index[0]]])
        auxiliary_line_condition = (p[0] < start_point_neck[0][0])
        return auxiliary_line_condition


class RisingWedge(AbstractPattern):
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
        result = (p[0] < p[1]) & (p[1] < p[3]) & (p[1] > p[2]) & (p[2] < p[3]) & (p[3] > p[4]) & (p[4] > p[2]) & (
                    p[2] > p[0]) & (p[4] > p[2])
        return result

    def check_time_condition(self, window: pd.DataFrame):
        result = (window.iloc[2].name - window.iloc[0].name) > (window.iloc[4].name - window.iloc[2].name)
        return result

    def check_auxiliary_line_condition(self, p: pd.DataFrame, window: pd.DataFrame):
        cx, cy = get_crosspt(window.iloc[1].name, p[1], window.iloc[3].name, p[3],
                             window.iloc[0].name, p[0], window.iloc[2].name, p[2])
        chart_length = (window.iloc[-1].name - window.iloc[0].name)
        triangle_length = (cx - window.iloc[-1].name)
        down_model = LinearRegression()
        down_line = pd.DataFrame([[window.iloc[0].name, p[0]], [window.iloc[2].name, p[2]]])
        down_model.fit(down_line[[0]], down_line[[1]])
        target = down_model.predict([[window.index[4]]])
        auxiliary_line_condition = (p[4] < target[0][0]) & (chart_length > triangle_length)
        return auxiliary_line_condition


class FallingWedge(AbstractPattern):
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
        result: Union[bool, int] = (p[0] > p[1]) & (p[1] > p[3]) & (p[1] < p[2]) & (p[2] > p[3]) &\
                                   (p[3] < p[4]) & (p[4] < p[2]) & (p[2] < p[0]) & (p[4] < p[2])
        return result

    def check_time_condition(self, window: pd.DataFrame):
        result = (window.iloc[2].name - window.iloc[0].name) > (window.iloc[4].name - window.iloc[2].name)
        return result

    def check_auxiliary_line_condition(self, p: pd.DataFrame, window: pd.DataFrame):
        cx, cy = get_crosspt(window.iloc[1].name, p[1], window.iloc[3].name, p[3],
                             window.iloc[0].name, p[0], window.iloc[2].name, p[2])
        chart_length = (window.iloc[-1].name - window.iloc[0].name)
        triangle_length = (cx - window.iloc[-1].name)
        upper_model = LinearRegression()
        upper_line = pd.DataFrame([[window.iloc[0].name, p[0]], [window.iloc[2].name, p[2]]])
        upper_model.fit(upper_line[[0]], upper_line[[1]])
        target = upper_model.predict([[window.index[4]]])
        auxiliary_line_condition = (p[4] > target[0][0]) & (chart_length > triangle_length)
        return auxiliary_line_condition


class DoubleBottom(AbstractPattern):
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

        # ++result = (p[0]>p[1])&(p[0]>p[2])&(p[2]>p[1])&(p[4]>p[2])
        result = (scaled_p[1][0] < 0.06) & (scaled_p[3][0] < 0.06)

        return result

    def check_time_condition(self, window: pd.DataFrame):
        condition1 = (window.iloc[2].name - window.iloc[0].name) * 1.5 > (window.iloc[4].name - window.iloc[2].name)
        condition2 = (window.iloc[2].name - window.iloc[0].name) < (window.iloc[4].name - window.iloc[2].name) * 1.5
        result = condition1 & condition2
        return result

    def check_auxiliary_line_condition(self, p: pd.DataFrame, window: pd.DataFrame):
        auxiliary_line_condition = True
        return auxiliary_line_condition


class DoubleTop(AbstractPattern):
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

        result = (scaled_p[1][0] > 0.94) & (scaled_p[3][0] > 0.94)

        return result

    def check_time_condition(self, window: pd.DataFrame):
        condition1 = (window.iloc[2].name - window.iloc[0].name) * 1.5 > (window.iloc[4].name - window.iloc[2].name)
        condition2 = (window.iloc[2].name - window.iloc[0].name) < (window.iloc[4].name - window.iloc[2].name) * 1.5
        result = condition1 & condition2
        return result

    def check_auxiliary_line_condition(self, p: pd.DataFrame, window: pd.DataFrame):
        auxiliary_line_condition = True
        return auxiliary_line_condition


class AscendingTriangle(AbstractPattern):
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
        result = condition1 & condition2
        return result

    def check_time_condition(self, window: pd.DataFrame):
        result = True
        return result

    def check_auxiliary_line_condition(self, p: pd.DataFrame, window: pd.DataFrame):
        auxiliary_line_condition = True
        return auxiliary_line_condition


class DescendingTriangle(AbstractPattern):
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
        result = condition1 & condition2
        return result

    def check_time_condition(self, window: pd.DataFrame):
        result = True
        return result

    def check_auxiliary_line_condition(self, p: pd.DataFrame, window: pd.DataFrame):
        auxiliary_line_condition = True
        return auxiliary_line_condition


class BullishTriangle(AbstractPattern):
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
        result = condition1 & condition2
        return result

    def check_time_condition(self, window: pd.DataFrame):
        result = True
        return result

    def check_auxiliary_line_condition(self, p: pd.DataFrame, window: pd.DataFrame):
        auxiliary_line_condition = True
        return auxiliary_line_condition


class BearishTriangle(AbstractPattern):
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
        result = condition1 & condition2
        return result

    def check_time_condition(self, window: pd.DataFrame):
        result = True
        return result

    def check_auxiliary_line_condition(self, p: pd.DataFrame, window: pd.DataFrame):
        auxiliary_line_condition = True
        return auxiliary_line_condition
