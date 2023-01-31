# -*- coding: utf-8 -*-
# utils by wukesonguo
# notebook: notebook-stock-division
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
    # step 1
    _stock_newest = load_newest_stock(n_current_date)
    _stock_newest = load_stock_sector(_stock_newest)
    _stock_newest = load_sw_industry(_stock_newest)
    _columns = [u'secID', u'secShortName', u's_listDate', u'listDateDeltaStatic', u'int_listDateDeltaStatic',
                u'tickerPrefixH2', u'shareCapitalRatio', u"totalStock",
                u'hs300', u'zx100', u'zx300',
                u'sh100', u'sh180', u'sh380',
                u'sz100', u'sz200', u'sz300',
                u'zz100', u'zz500', u'zz1000',
                u'sw_lev1_name_joint', u'sw_lev2_name_joint', u'sw_lev3_name_joint']
    _stock_newest = _stock_newest[_columns]
    # calculate stock_sw_level_name
    stock_sw_level_name = dict()
    for _lev in [1, 2, 3]:
        _lev_names_joint = "sw_lev{}_name_joint".format(_lev)
        stock_sw_level_name["sw_lev{}".format(_lev)] = _stock_newest[_lev_names_joint].unique()
        print(_stock_newest[_lev_names_joint].value_counts())

    print(len(_stock_newest))
    print(len(_stock_newest[_stock_newest['listDateDeltaStatic'] >= 2]))
    print(len(_stock_newest[_stock_newest['listDateDeltaStatic'] >= 4]))
    print(len(_stock_newest[_stock_newest['listDateDeltaStatic'] >= 10]))
    _stock_newest = _stock_newest[_stock_newest['listDateDeltaStatic'] >= 4]  # stock selection

    # # step 2
    # for _lev in [1, 2, 3]:
    #     _lev_names_joint = "sw_lev{}_name_joint".format(_lev)
    #     # print(_lev_names_joint)
    #     for _sw_lev_name in stock_sw_level_name["sw_lev{}".format(_lev)]:
    #         save_lev_name = "lev{}-{}-{}.csv".format(_lev, _sw_lev_name, n_current_date)
    #         print(save_lev_name)
    stock_tmp = []
    stock_sw_lev_tmp = []
    tmp_lev = 1
    for idx, n_current_date in enumerate(N_XSHG_DATES):
        if idx % 60 == 0: print(idx)
        stock_newest = copy.deepcopy(_stock_newest)
        stock_newest = load_base_indicator(stock_newest, str(n_current_date))
        # stock_newest = stock_newest[stock_newest[_lev_names_joint] == _sw_lev_name]
        stock_newest = load_detail_indicator(stock_newest, str(n_current_date))
        stock_newest = stock_newest.sort_values(by="tradeMarketValue", ascending=False)
        stock_newest = stock_value_investment(stock_newest)
        stock_tmp.append(copy.deepcopy(stock_newest))
        calcu_stock_sw_indicator(stock_newest, tmp_lev, stock_sw_lev_tmp, n_current_date)
    stock_tmp = pd.concat(stock_tmp)
    stock_tmp.to_csv('stock_indicator_tmp.csv', encoding='utf_8_sig')

    # # step 3
    print(len(stock_sw_lev_tmp))
    sw_lev_items = pd.concat(stock_sw_lev_tmp)
    sw_lev_items = sw_lev_items.reset_index()
    # print(sw_lev_items.head(10))
    sw_lev_items.to_csv('sw_lev{}_items.csv'.format(tmp_lev), encoding='utf_8_sig')
    for sw_levx_name in sw_lev_items["sw_lev{}_name_joint".format(tmp_lev)].unique():
        _sw_lev_item = copy.deepcopy(sw_lev_items[sw_lev_items["sw_lev{}_name_joint".format(tmp_lev)] == sw_levx_name])
        print(sw_levx_name)
        print(_sw_lev_item.head(5))
        _sw_lev_item["close_price_rise_rate_cum"] = np.cumprod(_sw_lev_item["close_price_rise_rate"])
        _sw_lev_item["close_price_rise_rate_weight_cum"] = np.cumprod(_sw_lev_item["close_price_rise_rate_weight"])
        _sw_lev_item.to_csv("total_stock_indicator.csv", encoding='utf_8_sig')
        plt.title("turnoverValue")
        _sw_lev_item.turnoverValue.ewm(span=10).mean().plot()
        _sw_lev_item.turnoverValue.ewm(span=20).mean().plot()
        _sw_lev_item.turnoverValue.ewm(span=60).mean().plot()
        plt.show()
        plt.title("turnoverRate")
        _sw_lev_item.turnoverRate.ewm(span=5).mean().plot()
        plt.show()
        plt.title("turnoverRateWeight")
        _sw_lev_item.turnoverRateWeight.ewm(span=5).mean().plot()
        plt.show()
        plt.title("totTurnoverValueProportion")
        _sw_lev_item.totTurnoverValueProportion.ewm(span=5).mean().plot()
        plt.show()
        plt.title("totTradeMarketValueProportion")
        _sw_lev_item.totTradeMarketValueProportion.ewm(span=5).mean().plot()
        plt.show()
        plt.title("turnover2market_rate")
        _sw_lev_item.turnover2market_rate.ewm(span=5).mean().plot()
        plt.show()
        plt.title("PE")
        _sw_lev_item.PE.ewm(span=5).mean().plot()
        plt.show()
        plt.title("PEWeight")
        _sw_lev_item.PEWeight.ewm(span=5).mean().plot()
        plt.show()
        plt.title("close_price_rise_rate_cum")
        _sw_lev_item.close_price_rise_rate_cum.ewm(span=5).mean().plot()
        plt.show()
        plt.title("close_price_rise_rate_weight_cum")
        _sw_lev_item.close_price_rise_rate_weight_cum.ewm(span=5).mean().plot()
        plt.show()
