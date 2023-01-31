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

def load_newest_stock():
	# 获取上市股票集合 上市状态为最新数据
	_field = [
		# 证券ID # 交易代码 # 证券简称 # 上市板块编码: 1-主板；2-创业板；4-科创板；5-北交所
		u'secID', u'ticker', u'secShortName', u'ListSectorCD',
		# 上市日期 # 总股本(最新)  # 公司无限售流通股份合计(最新)
		u'listDate', 'totalShares', 'nonrestFloatShares'
	]
	# A-沪深A股 L-上市
	stock_base = DataAPI.EquGet(secID=u"", ticker=u"", equTypeCD=u"A", listStatusCD=u"L", exchangeCD="",
								ListSectorCD=[1, 2, 4], field=_field, pandas="1")
	stock_base.insert(stock_base.shape[1], "shareCapitalRatio", 0)
	stock_base.shareCapitalRatio = stock_base.nonrestFloatShares / stock_base.totalShares
	return stock_base

def load_base_indicator(stock_base, current_day="20221216"):
	# secID have to be in stock_base !
	# current_day="20221216"
	stock_secIDs = stock_base.secID.to_dict().values()
	# 沪深股票前复权行情
	_field = [
		u'secID', u'tradeDate',
		u'preClosePrice', u'openPrice', u'highestPrice', u'lowestPrice', u'closePrice',
		u'turnoverVol', u'turnoverValue', u'turnoverRate', u'dealAmount', 
		u'marketValue', u'negMarketValue', u'accumAdjFactor', u'isOpen'
	]
	# 沪深股票前复权行情
	_stock_base = DataAPI.MktEqudAdjGet(secID=stock_secIDs, ticker=u"", tradeDate=current_day, beginDate=u"",
										endDate=u"", isOpen=1, field=_field, pandas="1")
	_stock_base.rename(columns={'negMarketValue': "tradeMarketValue"}, inplace=True)
	stock_base = pd.merge(stock_base, _stock_base, how='left', on='secID')
	stock_base.drop_duplicates(subset="secID", keep="first", inplace=True)
	return stock_base

# if __name__ == "__main__":
stock_newest = load_newest_stock()
stock_newest = load_base_indicator(stock_newest, str(s_last_date))

print(stock_newest.ListSectorCD.value_counts())
print(stock_newest.head(5))

# 随机在主板筛选股票测试
def replace_str_date(x):
    return int(x.replace("-", ""))
stock_newest_random = stock_newest[stock_newest["ListSectorCD"] == 1]
stock_newest_random["n_listDate"] = stock_newest_random["listDate"].apply(lambda x: replace_str_date(x))
stock_newest_random = stock_newest_random[stock_newest_random["n_listDate"] <= n_ten_year_date]
stock_newest_random = stock_newest_random[stock_newest_random["tradeMarketValue"] <= 2.0e+10]  # 200亿
stock_newest_random = stock_newest_random[stock_newest_random["tradeMarketValue"] >= 0.5e+10]  # 50亿
print(stock_newest_random.ListSectorCD.value_counts())
# stock_newest_random_secID = list(stock_newest_random.secID)
# random.shuffle(stock_newest_random)
# stock_newest_random_secID = stock_newest_random_secID[:50]
# print(stock_newest_random_secID)
