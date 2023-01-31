# -*- coding: utf-8 -*-
# utils by wukesonguo
import numpy as np
import pandas as pd

import json
import copy
import datetime

from matplotlib import pyplot as plt

from stock_tech_items import stock_newest_features, stock_tech_items_dict, base_dir
from calcu_tech_indicators import *

pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_columns', 1000)
pd.set_option('display.width', 1000)

if __name__ == "__main__":
    #
    stock_tech_items_list = []
    for secID, stock_tech_item in stock_tech_items_dict.items():

        stock_tech_item = calcu_base_indicator(stock_tech_item)     
        stock_tech_item = calcu_close_price_factor(stock_tech_item)   

        stock_tech_item["select_bear_market_factor_sum_0"] = stock_tech_item["select_bear_market_factor_sum_0"].apply(
            lambda x: 0 if x <= 4 else 1)
        stock_tech_item["select_bull_market_factor_sum_1"] = stock_tech_item["select_bull_market_factor_sum_1"].apply(
            lambda x: 0 if x <= 4 else 1)

        stock_tech_item = calcu_transaction_profit(secID, stock_tech_item)
        stock_tech_item = stock_tech_item.reset_index()

        stock_tech_item = merge_transaction_profit(secID, stock_tech_item)
        stock_tech_item = stock_tech_item.reset_index()

        stock_tech_items_list.append(stock_tech_item)

    stock_tech_item_concat = pd.concat(stock_tech_items_list)
    stock_tech_item_concat.head(10)

    _field = [
        "secID",
        "s_tradeDate0", "closePrice0", "s_tradeDate1", "closePrice1",
        # "cp_120days_1x_gradient", "cp_250days_1x_gradient",
        "profit", "bull_or_bear"
    ]
    stock_tech_item_concat = stock_tech_item_concat[_field]
    stock_tech_item_concat.to_csv('{}\data\csv\{}'.format(base_dir, "stock_tech_indicator_res.csv"), encoding='utf_8_sig')

    #
    _stock_mer_results = []
    stock_tech_item_concat = pd.read_csv("{}\{}".format(base_dir, "stock_tech_indicator_res.csv"))
    for secID in stock_tech_item_concat.secID.unique():
        _stock_mer_result = stock_tech_item_concat[stock_tech_item_concat["secID"] == secID]
        _stock_mer_result = merge_transaction_profit(secID, _stock_mer_result)
        _len = len(_stock_mer_result["secID"])
        _stock_mer_result["r_idx"] = pd.Series([_ for _ in range(_len)])
        _stock_mer_result["r_idx"] = _stock_mer_result["r_idx"].apply(lambda x:  _len - x - 1)
        _stock_mer_results.append(_stock_mer_result)
    stock_mer_result = pd.concat(_stock_mer_results)
    stock_mer_result["riseUpRate"] = stock_mer_result["closePrice1"] / stock_mer_result["closePrice0"]
    # stock_mer_result.drop(["Unnamed: 0", "cp_120days_1x_gradient", "cp_250days_1x_gradient", "profit"], axis=1, inplace=True)
    stock_mer_result.drop(["Unnamed: 0", "profit"], axis=1, inplace=True)
    stock_mer_result["s_tradeDate1"] = stock_mer_result["s_tradeDate1"].apply(
        lambda x: "2023-01-20" if x == "0" else x)  # 手工替换 s_tradeDate1
    stock_mer_result["dateDelta"] = stock_mer_result[["s_tradeDate1", "s_tradeDate0"]].apply(
        lambda x: half_year_transform(x), axis=1)

    stock_mer_result["realBull"] = stock_mer_result[["riseUpRate", "dateDelta"]].apply(
        lambda x: 1 if (x[0] >= 1.50) and (x[1] >= 1.5) else 0, axis=1)
    stock_mer_result["realBear"] = stock_mer_result[["riseUpRate", "dateDelta"]].apply(
        lambda x: 1 if (x[0] <= 0.75) and (x[1] >= 1.5) else 0, axis=1)
    stock_mer_result["nextRiseUpRate"] = stock_mer_result["riseUpRate"].shift(-1)
    stock_mer_result["nextRiseUpRate"].fillna(0, inplace=True)

    stock_mer_result["nextRiseUpRateLev"] = stock_mer_result["nextRiseUpRate"].apply(
        lambda x: 3 if x >= 1.2 else 2 if x >= 1.1 else 1 if x >= 1.02 else 0
                    if x >= 0.98 else -1 if x>= 0.9 else -2 if x >= 0.8 else -3)
    _stock_mer_bull_result = stock_mer_result[stock_mer_result["realBull"] == 1]
    print(_stock_mer_bull_result["nextRiseUpRateLev"].value_counts())
    _stock_mer_bear_result = stock_mer_result[stock_mer_result["realBear"] == 1]
    print(_stock_mer_bear_result["nextRiseUpRateLev"].value_counts())

    stock_mer_result.to_csv('{}\{}'.format(base_dir, "stock_tech_indicator_merge_res.csv"), encoding='utf_8_sig')
