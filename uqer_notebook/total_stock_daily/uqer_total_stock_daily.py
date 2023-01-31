# -*- coding: utf-8 -*-
# utils by wukesonguo
import numpy as np
import pandas as pd

import json
import copy
from matplotlib import pyplot as plt

pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_columns', 1000)
pd.set_option('display.width', 1000)

from uqer_datetime import *
from load_indicator_daily import *

if __name__ == "__main__":
    stock_newest = load_newest_stock()
    stock_newest = load_base_indicator(stock_newest, str(n_current_date))  # n_last_date
    stock_newest = load_stock_sector(stock_newest)
    stock_newest = load_sw_industry(stock_newest)
    stock_newest = load_detail_indicator(stock_newest, str(n_current_date))
    # for idx in range(50):
    #     print (stock_newest[100*idx: 100*(idx + 1)].to_dict())

    # 
    _pd_sw_id1 = pd.get_dummies(stock_newest["industryID1"], prefix="sw_id1")
    _pd_sw_id2 = pd.get_dummies(stock_newest["industryID2"], prefix="sw_id2")
    _pd_sw_id3 = pd.get_dummies(stock_newest["industryID3"], prefix="sw_id3")
    stock_newest = pd.concat([stock_newest, _pd_sw_id1], axis=1)
    stock_newest = pd.concat([stock_newest, _pd_sw_id2], axis=1)
    stock_newest = pd.concat([stock_newest, _pd_sw_id3], axis=1)

    stock_newest = dataframe_add_columns(stock_newest, ["ALL"], [1])
    print(list(stock_newest[stock_newest["zz1000"] == 1].secID))

    stock_select = stock_value_investment(stock_newest, stock_sector='zz1000', sw_industry='ALL')
    stock_select.drop_duplicates(subset="secShortName", keep="first", inplace=True)
    print(stock_select.shape)  # (115, 465)

    # # 
    # print(list(stock_select.secID))

    # print(", ".join(list(set(stock_newest.industryName1))))
    # print(", ".join(list(set(stock_newest.industryName2))))
    # print(", ".join(list(set(stock_newest.industryName3))))
    # print(" ")

    # # select_indus_level1 = []
    # # select_indus_level2 = []
    # # select_indus_level3 = []

    # # exclude_indus_level1 = []
    # # exclude_indus_level2 = []
    # # exclude_indus_level3 = []
