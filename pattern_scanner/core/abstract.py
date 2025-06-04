"""Base class defining the interface for candlestick pattern detection."""

from abc import *
import numpy as np
import pandas as pd
from .util import get_crosspt
from collections import defaultdict
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from sklearn.linear_model import LinearRegression
from mpl_finance import candlestick_ohlc



class AbstractPattern(metaclass=ABCMeta):
    """Base class for all candlestick chart patterns."""
    name = '패턴 이름'
    start_price = '지그재그 시작점의 가격타입(고가/저가)'
    pattern_type = '보조선타입(일직선 :0 / 상방하방형 :1)'
    condition = '조건식'
    zigzag_df = 'zizag 꼭지점 DF'
    test = 'test'

    def get_second_price(self):
        """Return the alternate price type used for odd/even zigzag points."""
        second_price = 'low'
        if self.start_price == 'low':
            second_price = 'high'
        return second_price

    @abstractmethod
    def check_point_condition(self, point_value_list: list):
        """Return True if price points satisfy the specific pattern shape."""
        pass

    @abstractmethod
    def check_time_condition(self, window: pd.DataFrame):
        """Return True if the time spans between points are valid."""
        pass

    @abstractmethod
    def check_auxiliary_line_condition(self, p: pd.DataFrame, window: pd.DataFrame):
        """Return True if additional line conditions for the pattern are met."""
        pass

    def check_pattern(self):
        """Scan the zigzag points and return detected pattern information."""
        zigzag_point = self.zigzag_df

        p = [''] * self.point_num
        pattern_list = []

        for i in range(self.point_num, len(zigzag_point) + 1):
            window = zigzag_point.iloc[i - self.point_num:i]  # sliding window
            p[0::2] = window[self.start_price].iloc[0::2]
            p[1::2] = window[self.second_price].iloc[1::2]

            type_list = [self.start_price, self.second_price] * self.point_num

            point_condition = self.check_point_condition(p)
            time_condition = self.check_time_condition(window)

            if (point_condition) & (time_condition):

                auxiliary_line_condition = self.check_auxiliary_line_condition(p, window)

                if self.pattern_type == 1:
                    cx, cy = get_crosspt(window.index[0], p[0], window.index[2], p[2],
                                         window.index[1], p[1], window.index[3], p[3])
                    line_fitter = LinearRegression()

                    bd = pd.DataFrame([[window.index[1], p[1]], [window.index[3], p[3]]])
                    line_fitter.fit(bd[[0]], bd[[1]])
                    la = line_fitter.predict([[window.index[0]]])
                elif self.pattern_type == 0:
                    cx, cy = np.nan, np.nan
                    la, bd = np.nan, np.nan

                if auxiliary_line_condition:
                    patterns = defaultdict(list)
                    patterns['pattern_name'] = self.__class__.__name__
                    patterns['interval'] = "1m"
                    patterns['cxcy'] = [cx, cy]
                    patterns['labd'] = [la, bd]
                    patterns['point'].append(
                        [{'index': window.index[i], 'type': type_list[i]} for i in range(len(window.index))])
                    patterns['point'] = patterns['point'][0]
                    pattern_list.append(patterns)
        return pattern_list

    def make_plot(self):
        """Visualize detected patterns using candlestick and volume charts."""
        pattern_list = self.check_pattern()
        df = self.candle_df
        for pattern in pattern_list[:]:
            l = pattern['point'][0]['index']
            r = pattern['point'][-1]['index']
            cx = pattern["cxcy"][0]
            cy = pattern["cxcy"][1]
            la = pattern["labd"][0]
            bd = pattern["labd"][1]
            t = 50

            # 캔들스틱 차트 + 거래량 표시=====================================================
            fig = plt.figure(figsize=(8, 5))
            fig.set_facecolor('w')
            gs = gridspec.GridSpec(2, 1, height_ratios=[3, 1])
            axes = []
            axes.append(plt.subplot(gs[0]))
            axes.append(plt.subplot(gs[1], sharex=axes[0]))
            axes[0].get_xaxis().set_visible(False)

            plot_df = df.loc[l - t:r + t]
            x = plot_df.index
            ohlc = plot_df[['open', 'high', 'low', 'close']].astype(int).values
            dohlc = np.hstack((np.reshape(x, (-1, 1)), ohlc))
            # 봉차트
            candlestick_ohlc(axes[0], dohlc, width=0.5, colorup='r', colordown='b', alpha=.7)

            # 거래량 차트
            axes[1].bar(x, plot_df.volume, color='k', width=0.6, align='center')

            # 지그재그 직선 표시==============================================================
            for i in range(0, len(pattern['point']) - 1):
                first_index = pattern['point'][i]['index']
                first_price_tag = pattern['point'][i]['type']
                second_index = pattern['point'][i + 1]['index']
                second_price_tag = pattern['point'][i + 1]['type']
                axes[0].plot(plot_df.loc[[first_index, second_index]].index,
                             [plot_df[first_price_tag].loc[first_index], plot_df[second_price_tag].loc[second_index]],
                             color='black', marker='o', markersize=3)
            # 보조선 표시
            if self.pattern_type == 1:
                axes[0].plot([pattern['point'][0]['index'], cx],
                             [plot_df[self.start_price].loc[pattern['point'][0]['index']], cy],
                             color='green', alpha=1)
                axes[0].plot([pattern['point'][1]['index'], cx],
                             [plot_df[self.second_price].loc[pattern['point'][1]['index']], cy],
                             color='green', alpha=1)

            plt.tight_layout()
            plt.show()
