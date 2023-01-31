# -*- coding: utf-8 -*-
# utils by wukesonguo
# notebook: feature_mining_pipeline
import numpy as np
import pandas as pd

import json
import copy
import datetime

from matplotlib import pyplot as plt

from uqer_datetime import *
from load_indicator_daily import *
from short_term_trends_annotation import *

pd.set_option('display.max_rows', 10000)
pd.set_option('display.max_columns', 10000)
pd.set_option('display.width', 10000)

if __name__ == "__main__":
    # step 0
    stock_newest = load_newest_stock()
    stock_newest = load_base_indicator(stock_newest, "20221222")
    stock_newest = load_stock_sector(stock_newest)
    stock_newest = load_sw_industry(stock_newest)
    stock_newest = load_detail_indicator(stock_newest, "20221222")
    # for idx in range(50):
    #     print (stock_newest[100*idx: 100*(idx+1)].to_dict())

    _pd_sw_id1 = pd.get_dummies(stock_newest["industryID1"], prefix="sw_id1")
    _pd_sw_id2 = pd.get_dummies(stock_newest["industryID2"], prefix="sw_id2")
    _pd_sw_id3 = pd.get_dummies(stock_newest["industryID3"], prefix="sw_id3")
    stock_newest = pd.concat([stock_newest, _pd_sw_id1], axis=1)
    stock_newest = pd.concat([stock_newest, _pd_sw_id2], axis=1)
    stock_newest = pd.concat([stock_newest, _pd_sw_id3], axis=1)

    stock_newest = dataframe_add_columns(stock_newest, ["ALL"], [1])
    # stock_select = stock_value_investment(stock_newest, stock_sector='zz1000', sw_industry='ALL')
    # stock_select.drop_duplicates(subset="secShortName", keep="first", inplace=True)
    # # print(stock_select.shape)

    # step 1
    _stock_newest = stock_newest[stock_newest["zz1000"] == 1]
    _stock_newest = _stock_newest[_stock_newest["tradeMarketValue"] <= 12500000000]
    _stock_newest = _stock_newest[_stock_newest["tradeMarketValue"] >= 7500000000]
    stock_secIDs = list(_stock_newest.secID)
    print(len(stock_secIDs))
    print(_stock_newest[
              ["secShortName", "industryName1", "industryName2", "industryName3", "closePrice", "DilutedEPS", "EGRO",
               "tradeMarketValue"]])

    print("Done.")
