# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd

import json
import copy
import random
from matplotlib import pyplot as plt


def calcu_close_price_factor(stock_rdate_item):
    # 组合均线策略 technical indicators & factors
    # essential: ["openPrice",  "highestPrice",  "lowestPrice",  "closePrice", "turnoverRate", "dealAmount"]
    stock_rdate_item_factor = dict()
    for secID, _item in stock_rdate_item.items():
        stock_item = copy.deepcopy(_item)
        stock_item["rectifyPrice"] = stock_item[["openPrice",  "highestPrice",  "lowestPrice",  "closePrice"]].mean(axis=1)  # calcu average price
        stock_item["closePrice"] = stock_item["rectifyPrice"]

        ma_days = [5, 10, 20, 60, 120, 250]
        # technical indicator
        for _day in ma_days:
            stock_item["mean_closePrice_{}days".format(_day)] = stock_item.closePrice.rolling(_day).mean()
            stock_item["variance_closePrice_{}days".format(_day)] = stock_item.closePrice.rolling(_day).std()

        for _day in ma_days:
            stock_item["mean_turnoverRate_{}days".format(_day)] = stock_item.turnoverRate.rolling(_day).mean()
            stock_item["variance_turnoverRate_{}days".format(_day)] = stock_item.turnoverRate.rolling(_day).std()

        for _day in ma_days:
            stock_item["mean_dealAmount_{}days".format(_day)] = stock_item.dealAmount.rolling(_day).mean()
            stock_item["variance_dealAmount_{}days".format(_day)] = stock_item.dealAmount.rolling(_day).std()

        for _day in ma_days:
            stock_item["mean_closePrice_{}days_1x_variance".format(_day)] = stock_item["mean_closePrice_{}days".format(_day)] + stock_item["variance_closePrice_{}days".format(_day)]
            stock_item["mean_closePrice_{}days_2x_variance".format(_day)] = stock_item["mean_closePrice_{}days".format(_day)] + 2 * stock_item["variance_closePrice_{}days".format(_day)]
        
        calcu_gradient_day = 5
        for _day in ma_days:
            stock_item["mean_closePrice_{}days_1x_gradient".format(_day)] = stock_item["mean_closePrice_{}days".format(_day)].rolling(calcu_gradient_day).apply(lambda y: np.polyfit(np.arange(len(y)), y, 1)[0])
            stock_item["mean_closePrice_{}days_2x_gradient".format(_day)] = stock_item["mean_closePrice_{}days".format(_day)].rolling(calcu_gradient_day).apply(lambda y: np.polyfit(np.arange(len(y)), y, 2)[0])

        stock_item["mean_closePrice_1x_gradient"] = stock_item["closePrice"].rolling(calcu_gradient_day).apply(lambda y: np.polyfit(np.arange(len(y)), y, 1)[0])
        stock_item["mean_closePrice_2x_gradient"] = stock_item["closePrice"].rolling(calcu_gradient_day).apply(lambda y: np.polyfit(np.arange(len(y)), y, 2)[0])

        # factors
        for _day in ma_days:
            # 收盘价站上均线 & 均线Plus方差
            stock_item["select_{}days_0x_variance_factor".format(_day)] = stock_item["closePrice"] >= stock_item["mean_closePrice_{}days".format(_day)]
            stock_item["select_{}days_0x_variance_factor".format(_day)] = stock_item["select_{}days_0x_variance_factor".format(_day)].apply(lambda x: 0 if int(x) <= 0 else 1) 
            stock_item["select_{}days_1x_variance_factor".format(_day)] = stock_item["closePrice"] >= stock_item["mean_closePrice_{}days_1x_variance".format(_day)]
            stock_item["select_{}days_1x_variance_factor".format(_day)] = stock_item["select_{}days_1x_variance_factor".format(_day)].apply(lambda x: 0 if int(x) <= 0 else 1) 
            stock_item["select_{}days_1x_gradient_factor".format(_day)] = stock_item["mean_closePrice_{}days_1x_gradient".format(_day)].apply(lambda x: 0 if x <= 0 else 1)
            stock_item["select_{}days_2x_gradient_factor".format(_day)] = stock_item["mean_closePrice_{}days_2x_gradient".format(_day)].apply(lambda x: 0 if x <= 0 else 1)
        stock_item["select_1x_gradient_factor".format(_day)] = stock_item["mean_closePrice_1x_gradient".format(_day)].apply(lambda x: 0 if x <= 0 else 1)
        stock_item["select_2x_gradient_factor".format(_day)] = stock_item["mean_closePrice_2x_gradient".format(_day)].apply(lambda x: 0 if x <= 0 else 1)

        # factors
        select_bull_market_factor_list = []
        for idx in range(len(ma_days) - 1):
            select_bull_market_factor_list.append("select_bull_market_factor_{}".format(idx))
            stock_item["select_bull_market_factor_{}".format(idx)] = stock_item["mean_closePrice_{}days".format(ma_days[idx+1])] <= stock_item["mean_closePrice_{}days".format(ma_days[idx])]
            stock_item["select_bull_market_factor_{}".format(idx)] = stock_item["select_bull_market_factor_{}".format(idx)].apply(lambda x: 0 if int(x) <= 0 else 1) 
        # stock_item["select_bull_market_factor_0"] = stock_item["select_bull_market_factor_0"].apply(lambda x: 1)  # 是否考虑 cp_ma5 > cp_ma10
        for idx in range(len(ma_days) - 1):
            stock_item["select_bull_market_factor_sum_{}".format(idx)] = stock_item[select_bull_market_factor_list].sum(axis=1)
            stock_item["select_bull_market_factor_sum_{}".format(idx)] = stock_item["select_bull_market_factor_sum_{}".format(idx)].apply(lambda x: x + idx)
            select_bull_market_factor_list.pop()  # 正常的穿越顺序为从短期到长期依次穿越
        # stock_item["select_bull_market_factor"] = stock_item["select_bull_market_factor"].apply(lambda x: 0 if int(x) <= (len(ma_days) - 1) else 1)

        select_bear_market_factor_list = []
        for idx in range(len(ma_days) - 1):
            select_bear_market_factor_list.append("select_bear_market_factor_{}".format(idx))
            stock_item["select_bear_market_factor_{}".format(idx)] = stock_item["mean_closePrice_{}days".format(ma_days[idx+1])] >= stock_item["mean_closePrice_{}days".format(ma_days[idx])]
            stock_item["select_bear_market_factor_{}".format(idx)] = stock_item["select_bear_market_factor_{}".format(idx)].apply(lambda x: 0 if int(x) <= 0 else 1) 
        # stock_item["select_bear_market_factor_0"] = stock_item["select_bear_market_factor_0"].apply(lambda x: 1)  # 是否考虑 cp_ma5 > cp_ma10
        for idx in range(len(ma_days) - 1):
            stock_item["select_bear_market_factor_sum_{}".format(idx)] = stock_item[select_bear_market_factor_list].sum(axis=1)
            stock_item["select_bear_market_factor_sum_{}".format(idx)] = stock_item["select_bear_market_factor_sum_{}".format(idx)].apply(lambda x: x + idx)
            select_bear_market_factor_list.pop()  # 正常的穿越顺序为从短期到长期依次穿越
        # stock_item["select_bear_market_factor"] = stock_item["select_bear_market_factor"].apply(lambda x: 0 if int(x) <= (len(ma_days) - 1) else 1)

        stock_rdate_item_factor[secID] = stock_item
        print(stock_item.tail(10))
    return stock_rdate_item_factor

# if __name__ == "__main__":
stock_rdate_item_factor = calcu_close_price_factor(stock_rdate_item)        
