# -*- coding: utf-8 -*-
# utils by wukesonguo
# notebook: notebook-2-sw-division
# indicator group by sw industry
# not use load_detail_indicator()
import numpy as np
import pandas as pd

import json
import copy
import datetime

from matplotlib import pyplot as plt

from uqer_datetime import *
from load_indicator_daily import *

pd.set_option('display.max_rows', 10000)
pd.set_option('display.max_columns', 10000)
pd.set_option('display.width', 10000)

if __name__ == "__main__":

    _stock_newest = load_newest_stock(n_current_date)
    _stock_newest = load_stock_sector(_stock_newest)
    _stock_newest = load_sw_industry(_stock_newest)

    _columns = [u'secID', u'tickerPrefixH2', u'secShortName', u'listDate', u'listDateDelta',
                u'nonrestFloatShares', u'totalShares', u'shareCapitalRatio',
                u'hs300', u'sh100', u'sh180', u'sh380', u'sz100', u'sz200', u'sz300',
                u'zz100', u'zz500', u'zz1000',
                u'sw_lev1_name_joint', u'sw_lev2_name_joint', u'sw_lev3_name_joint']
    _stock_newest = _stock_newest[_columns]

    stock_sw_level_name = dict()
    for _lev in [1, 2, 3]:
        _lev_names_joint = "sw_lev{}_name_joint".format(_lev)
        stock_sw_level_name["sw_lev{}".format(_lev)] = _stock_newest[_lev_names_joint].unique()

    for _lev in [1, 2, 3]:
        _lev_names_joint = "sw_lev{}_name_joint".format(_lev)
        # print(_lev_names_joint)
        for _sw_lev_name in stock_sw_level_name["sw_lev{}".format(_lev)]:
            save_lev_name = "lev{}-{}-{}.csv".format(_lev, _sw_lev_name, n_current_date)
            print(save_lev_name)
            stock_sw_level_temp = []
            for idx, current_date in enumerate(N_XSHG_DATES):
                stock_newest = copy.deepcopy(_stock_newest)
                stock_newest = load_base_indicator(stock_newest, str(current_date))
                stock_newest = stock_newest[stock_newest[_lev_names_joint] == _sw_lev_name]
                if idx == 0:
                    print("TradeMarketValueProportion:")
                    print(stock_newest.totTradeMarketValueProportion.sum())
                    print("TurnoverValueProportion:")
                    print(stock_newest.totTurnoverValueProportion.sum())
                # stock_newest = load_detail_indicator(stock_newest, str(current_date))
                stock_newest = stock_newest.sort_values(by="tradeMarketValue", ascending=False)
                calcu_stock_sw_indicator(stock_newest, _lev, stock_sw_level_temp, current_date)
            _sw_lev_item = pd.concat(stock_sw_level_temp)
            _sw_lev_item["close_price_rise_rate_cum"] = np.cumprod(_sw_lev_item["close_price_rise_rate"])
            _sw_lev_item["close_price_rise_rate_cum_weight"] = np.cumprod(_sw_lev_item["close_price_rise_rate_weight"])
            _sw_lev_item.to_csv('stock_sw_2_daily/{}'.format(save_lev_name), encoding='utf_8_sig')
            print(len(stock_newest.secShortName))
            print(stock_newest.secShortName.head(10))
            plt.title("turnoverValue")
            # _sw_lev_item.turnoverValue.ewm(span=5).mean().plot()
            _sw_lev_item.turnoverValue.ewm(span=10).mean().plot()
            _sw_lev_item.turnoverValue.ewm(span=20).mean().plot()
            _sw_lev_item.turnoverValue.ewm(span=60).mean().plot()
            # _sw_lev_item.turnoverValue.ewm(span=120).mean().plot()
            plt.show()
            plt.title("turnoverRate")
            _sw_lev_item.turnoverRate.ewm(span=5).mean().plot()
            plt.show()
            plt.title("turnoverRateWeight")
            _sw_lev_item.turnoverRateWeight.ewm(span=5).mean().plot()
            plt.show()
            plt.title("close_price_rise_rate_cum")
            _sw_lev_item.close_price_rise_rate_cum.ewm(span=5).mean().plot()
            plt.show()
            plt.title("close_price_rise_rate_cum_weight")
            _sw_lev_item.close_price_rise_rate_cum_weight.ewm(span=5).mean().plot()
            plt.show()
