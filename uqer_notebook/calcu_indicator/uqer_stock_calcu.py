# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd

import json
import copy
import random
from matplotlib import pyplot as plt

pd.set_option('display.max_rows', 10000)
pd.set_option('display.max_columns', 10000)
pd.set_option('display.width', 10000)

# load datetime periods

if __name__ == "__main__":
    # step 1 load_base_indicator.py
    stock_newest = load_newest_stock()
    stock_newest = load_base_indicator(stock_newest, str(s_last_date))
    print(stock_newest.ListSectorCD.value_counts())
    print(stock_newest.head(5))

    def replace_str_date(x):
        # from "1991-04-03" to 19910403
        return int(x.replace("-", ""))
    stock_newest_random = stock_newest[stock_newest["ListSectorCD"] == 1]
    stock_newest_random["n_listDate"] = stock_newest_random["listDate"].apply(lambda x: replace_str_date(x))
    stock_newest_random = stock_newest_random[stock_newest_random["n_listDate"] <= n_ten_year_date]
    stock_newest_random = stock_newest_random[stock_newest_random["tradeMarketValue"] <= 2.0e+10]  # 200亿
    stock_newest_random = stock_newest_random[stock_newest_random["tradeMarketValue"] >= 0.5e+10]  # 50亿
    print(stock_newest_random.ListSectorCD.value_counts())

    # step 2 load_detail_sector.py
    stock_newest_random = stock_newest_random.sample(n=50)  # 随机选择50支股票
    stock_newest_random = load_stock_sector(stock_newest_random)
    stock_newest_random = load_sw_industry(stock_newest_random)

    _pd_sw_id1 = pd.get_dummies(stock_newest_random["industryName1"], prefix="sw_id1")
    _pd_sw_id2 = pd.get_dummies(stock_newest_random["industryName2"], prefix="sw_id2")
    _pd_sw_id3 = pd.get_dummies(stock_newest_random["industryName3"], prefix="sw_id3")
    stock_newest_random = pd.concat([stock_newest_random, _pd_sw_id1], axis=1)
    stock_newest_random = pd.concat([stock_newest_random, _pd_sw_id2], axis=1)
    stock_newest_random = pd.concat([stock_newest_random, _pd_sw_id3], axis=1)

    print(stock_newest_random.index)
    stock_newest_random.head(5)    

    # step 3 load_detail_indicator.py
    stock_newest_random = load_detail_indicator(stock_newest_random, str(n_last_date))  # 增加指标
    stock_newest_random = dataframe_add_columns(stock_newest_random, ["ALL"], [1])
    stock_newest_random = stock_value_investment(stock_newest_random, stock_sector='zz1000', sw_industry='ALL')
    stock_newest_random.drop_duplicates(subset=['secShortName'], keep="first", inplace=True)
    print("\n")
    print(stock_newest_random)

    # step 4 load_daily_indicator.py
    # 从筛选的股票中增加时间区域股价 DataAPI.MktEqudAdjGet()
    stock_rdate_item = dict()  # stock_rdate_item[_secID] = res
    read_stock_base_read(stock_rdate_item)
    print(stock_rdate_item.keys())
    print(stock_rdate_item.values()[0].head(10))

    # step 5 calcu_boll_indicator.py
    stock_rdate_item_factor = calcu_boll_indicator(stock_rdate_item)      

    # step 6 calcu_trade_profit.py
    stock_factor_dict = calcu_transaction_profit(stock_rdate_item_factor)

    trade_list = []
    for factor in stock_factor_dict.keys():
        stock_item = stock_factor_dict[factor]
        for _ in range(len(stock_item)):
            trade_list.append((stock_item[_].secID[0], factor, stock_item[_].profit.sum()))
    trade_list = pd.DataFrame(trade_list, columns=["secID", "factor", "profit"])
    trade_list.sort_values(by="profit")

    # stop 7 plot_stock_indicator.py
