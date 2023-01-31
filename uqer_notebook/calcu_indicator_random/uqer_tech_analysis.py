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
        "cp_120days_1x_gradient", "cp_250days_1x_gradient",
        "profit", "bull_or_bear"
    ]
    stock_tech_item_concat[_field].to_csv('{}\data\csv\{}'.format(base_dir, "stock_tech_indicator_res.csv"), encoding='utf_8_sig')
