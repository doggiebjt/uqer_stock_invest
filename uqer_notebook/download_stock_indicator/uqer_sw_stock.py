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

    _stock_newest = load_newest_stock(n_current_date)
    _stock_newest = load_stock_sector(_stock_newest)
    _stock_newest = load_sw_industry(_stock_newest)
    _stock_newest.to_csv('stock_load_newest_indicator.csv', encoding='utf_8_sig')
    # stock select
    _stock_newest = _stock_newest[_stock_newest["tickerPrefixH2"] != "68"]
    _stock_newest = _stock_newest[_stock_newest["tickerPrefixH2"] != "30"]
    _stock_newest = _stock_newest[_stock_newest["listDateDeltaStatic"] >= 2.0]  # 注意: 股票交易日期比股票上市日期早两年
    _columns = [u'secID', u'secShortName', u's_listDate',
                # u'listDateDeltaStatic', u'int_listDateDeltaStatic',
                # u'tickerPrefixH2', u'shareCapitalRatio',
                # u'hs300', u'zx100', u'zx300',
                # u'sh100', u'sh180', u'sh380',
                # u'sz100', u'sz200', u'sz300',
                # u'zz100', u'zz500', u'zz1000',
                # u'sw_lev1_name_joint', u'sw_lev2_name_joint', u'sw_lev3_name_joint'
                ]
    _stock_newest = _stock_newest[_columns]

    # stock select
    _stock_newest = _stock_newest.sample(n=200, replace=False, random_state=6688)

    # calculate stock_sw_level_name
    stock_sw_level_name_list = list()
    stock_sw_level_name_dict = dict()
    # for _lev in [1, 2, 3]:
    #     _lev_names_joint = "sw_lev{}_name_joint".format(_lev)
    #     stock_lev_names_joint = list(_stock_newest[_lev_names_joint].unique())
    #     stock_sw_level_name_list.extend(stock_lev_names_joint)
    # for idx, stock_lev_name in enumerate(stock_sw_level_name_list):
    #     stock_sw_level_name_dict[stock_lev_name] = idx
    # stock_sw_level_name_pandas = pd.DataFrame(stock_sw_level_name_dict, index=[0]).T
    # print(stock_sw_level_name_pandas.head(10))
    # stock_sw_level_name_pandas.to_csv('stock_sw_level_name_pandas.csv', encoding='utf_8_sig')

    # print(stock_sw_level_name_list[:10])

    for s_s_date, s_e_date in stock_periodic:
        print("stock indicator from {} to {}".format(s_s_date, s_e_date))
        n_s_date = str(s_s_date).replace("-", "")
        n_e_date = str(s_e_date).replace("-", "")
        S_XSHG_DATES, S_XSHE_DATES = extract_trade_dates(s_s_date, s_e_date)
        N_XSHG_DATES = [int(_.replace("-", "")) for _ in S_XSHG_DATES.calendarDate]
        print(len(N_XSHG_DATES))
        stock_tmp = []
        for idx, n_current_date in enumerate(N_XSHG_DATES):
            stock_newest = copy.deepcopy(_stock_newest)
            stock_newest = load_base_indicator(stock_newest, str(n_current_date))
            stock_newest = load_detail_indicator(stock_newest, str(n_current_date))
            stock_tmp.append(copy.deepcopy(stock_newest))
        stock_tmp = pd.concat(stock_tmp)
        # stock_tmp["sw_lev1_name_joint"] = stock_tmp["sw_lev1_name_joint"].apply(lambda x: stock_sw_level_name_dict[x])
        # stock_tmp["sw_lev2_name_joint"] = stock_tmp["sw_lev2_name_joint"].apply(lambda x: stock_sw_level_name_dict[x])
        # stock_tmp["sw_lev3_name_joint"] = stock_tmp["sw_lev3_name_joint"].apply(lambda x: stock_sw_level_name_dict[x])
        stock_tmp.to_csv(
            'stock_tech_indicator/stock_indicator_{}_to_{}.csv'.format(n_s_date, n_e_date), encoding='utf_8_sig')

        tech_1_field = [
            u'secID', u's_listDate', "tradeDate",
            u'openPrice', u'highestPrice', u'lowestPrice', u'closePrice', u'preClosePrice',
            u'turnoverVol', u'turnoverValue', u'turnoverRate', u'dealAmount',
            u'marketValue', u'tradeMarketValue'
        ]
        stock_tmp[tech_1_field].to_csv(
            'stock_tech_indicator/stock_tech_indicator_1_{}_to_{}.csv'.format(n_s_date, n_e_date), encoding='utf_8_sig')

        tech_2_field = [
            "secID", u's_listDate', "tradeDate",
            # 技术指标
            "EMA5", "EMA10", "EMA20", "EMA60", "EMA120",  # 均线
            "MA5", "MA10", "MA20", "MA60", "MA120",  # 均线
            # 动量因子&情绪类因子
            "VOL5", "VOL10", "VOL20", "VOL60", "VOL120",
            # "Volatility",  # 换手率相关
        ]
        stock_tmp[tech_2_field].to_csv(
            'stock_tech_indicator/stock_tech_indicator_2_{}_to_{}.csv'.format(n_s_date, n_e_date), encoding='utf_8_sig')