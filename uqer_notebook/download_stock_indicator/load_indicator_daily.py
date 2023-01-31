# -*- coding: utf-8 -*-
# utils by wukesonguo
import numpy as np
import pandas as pd

import json
import copy
import datetime

from matplotlib import pyplot as plt

def dataframe_add_columns(t_df, columns, res_data):
    # columns = ["jump_up_date", "jump_dn_date"]
    # res_data = [0, 0]
    for _col, _res in zip(columns, res_data):
        t_df = pd.concat([t_df, pd.DataFrame(columns=list('A'))])
        t_df.rename(columns={'A': _col}, inplace=True)
        t_df[_col] = t_df[_col].apply(lambda x: _res)
    return t_df

def half_year_transform(n_current_date, s_listDate):
    n_listDate = int(s_listDate.replace("-", ""))
    d1 = datetime.datetime.strptime(str(n_current_date), '%Y%m%d')
    d2 = datetime.datetime.strptime(str(n_listDate), '%Y%m%d')
    delta = d1 - d2
    n_delta = delta.days / 365.0
    return int(n_delta * 10) / 10.0

def load_newest_stock(n_current_date):
    # 获取上市股票集合
    _field = [
        # 证券ID # 交易代码 # 证券简称 # 上市板块编码: 1-主板；2-创业板；4-科创板；5-北交所
        u'secID', u'ticker', u'secShortName', u'ListSectorCD',
        # 上市日期 # 总股本(最新)  # 公司无限售流通股份合计(最新)
        u'listDate', 'totalShares', 'nonrestFloatShares'
    ]
    # A-沪深A股 L-上市
    stock_base = DataAPI.EquGet(secID=u"", ticker=u"", equTypeCD=u"A", listStatusCD=u"L", exchangeCD="", ListSectorCD=u"", field=_field,pandas="1")
    stock_base["shareCapitalRatio"] = 0
    stock_base.shareCapitalRatio = stock_base.nonrestFloatShares / stock_base.totalShares
    stock_base["listDateDeltaStatic"] = stock_base["listDate"].apply(lambda x: half_year_transform(n_current_date, x))
    stock_base["tickerPrefixH2"] = stock_base["secID"].apply(lambda x: x[:2])
    stock_base.rename(columns={'listDate': "s_listDate"}, inplace=True)
    stock_base["int_listDateDeltaStatic"] = stock_base["listDateDeltaStatic"].apply(lambda x: int(x))
    return stock_base

def load_base_indicator(stock_base, n_current_day="20221216"):
    # secID have to be in stock_base !
    # n_current_day="20221216"
    stock_secIDs = stock_base.secID.to_dict().values()
    # 沪深股票前复权行情
    # _field = [
    #     u'secID', u'tradeDate',
    #     u'preClosePrice', u'openPrice', u'highestPrice', u'lowestPrice', u'closePrice',
    #     u'turnoverVol', u'turnoverValue', u'turnoverRate', u'dealAmount', u'turnoverRate',
    #     u'marketValue', u'negMarketValue', u'accumAdjFactor', u'isOpen'
    # ]
    _field = [
        u'secID', u'tradeDate', u'preClosePrice',
        u'openPrice', u'highestPrice', u'lowestPrice', u'closePrice',
        u'turnoverVol', u'turnoverValue', u'turnoverRate', u'dealAmount',
        u'marketValue', u'negMarketValue'
    ]
    # 沪深股票前复权行情
    _stock_base = DataAPI.MktEqudAdjGet(secID=stock_secIDs, ticker=u"", tradeDate=n_current_day,
                                        beginDate=u"", endDate=u"", isOpen=1, field=_field, pandas="1")
    _stock_base.rename(columns={'negMarketValue': "tradeMarketValue"}, inplace=True)
    stock_base = pd.merge(stock_base, _stock_base, how='left', on='secID')
    stock_base.drop_duplicates(subset="secID", keep="first", inplace=True)
    # # stock_base["tradeMarketValueCalcu2"] = stock_base["nonrestFloatShares"] * stock_base["closePrice"]
    # stock_base["tickerPrefixH3"] = stock_base["secID"].apply(lambda x: x[:3])
    # tot_marketValue = stock_base.marketValue.sum()
    # tot_tradeMarketValue = stock_base.tradeMarketValue.sum()
    # tot_turnoverValue = stock_base.turnoverValue.sum()
    # stock_base["totMarketValueProportion"] = stock_base["marketValue"] / tot_marketValue
    # stock_base["totTradeMarketValueProportion"] = stock_base["tradeMarketValue"] / tot_tradeMarketValue
    # stock_base["totTurnoverValueProportion"] = stock_base["turnoverValue"] / tot_turnoverValue
    # stock_base['close_price_rise_rate'] = stock_base['closePrice'] / stock_base['preClosePrice']
    # stock_base["listDateDeltaDynamic"] = stock_base["s_listDate"].apply(lambda x: half_year_transform(n_current_day, x))
    # stock_base["int_listDateDeltaDynamic"] = stock_base["listDateDeltaDynamic"].apply(lambda x: int(x))
    return stock_base

def load_detail_indicator(stock_base, current_day="20221216"):
    # secID have to be in stock_base !
    # current_day = "20221216"
    stock_secIDs = stock_base.secID.to_dict().values()
    # 获取多只股票的因子数据
    # _field = [
    #     "secID", "tradeDate",
    #     # 价值因子&质量因子
    #     "CTOP", "CTP5", "ETOP", "ETP5", "ROE", "ROE5", "ROA", "ROA5", "PE", "PB", "PCF", "PS", "EPS", "DilutedEPS",
    #     "NetProfitRatio", "GrossIncomeRatio", "DEGM", "DebtsAssetRatio", "DebtEquityRatio", "LCAP",
    #     # 增长类指标
    #     "NetProfitGrowRate", "NetAssetGrowRate", "TotalProfitGrowRate", "TotalAssetGrowRate",
    #     "OperatingRevenueGrowRate", "EGRO",
    #     # 技术指标
    #     "EMA5", "EMA10", "EMA20", "EMA60", "EMA120", "MA5", "MA10", "MA20", "MA60", "MA120",  # 均线
    #     "MACD", "KDJ_K", "KDJ_D", "KDJ_J", "BollUp", "BollDown",
    #     # 动量因子&情绪类因子
    #     "VOL5", "VOL10", "VOL20", "VOL60", "VOL120", "DAVOL5", "DAVOL10", "DAVOL20", "Volatility",  # 换手率相关
    #     "REVS5", "REVS10", "REVS20",  # 股票的10日收益
    #     "FiftyTwoWeekHigh",  # 当前价格处于过去1年股价的位置
    #     "RSI",  # 相对强弱指标
    # ]
    _field = [
        "secID", "tradeDate",
        # # 价值因子&质量因子&增长类指标
        "CTOP", "CTP5", "ETOP", "ETP5",
        "ROE", "ROE5", "ROA", "ROA5", "PE", "PB", "PCF", "PS",
        "GrossIncomeRatio", "DEGM", "NetProfitRatio", "NetProfitGrowRate", "EGRO",
        "DebtsAssetRatio", "DebtEquityRatio", "LCAP", "DilutedEPS",
        # # 技术指标
        "EMA5", "EMA10", "EMA20", "EMA60", "EMA120",  # 均线
        "MA5", "MA10", "MA20", "MA60", "MA120",  # 均线
        # # 动量因子&情绪类因子
        "VOL5", "VOL10", "VOL20", "VOL60", "VOL120",
        # "DAVOL5", "DAVOL10", "DAVOL20",
        # "Volatility",  # 换手率相关
        # "REVS5", "REVS10", "REVS20",  # 股票的10日收益
        # "FiftyTwoWeekHigh",  # 当前价格处于过去1年股价的位置
    ]
    _stock_base = DataAPI.MktStockFactorsOneDayGet(secID=stock_secIDs, ticker=u"",
                                                   tradeDate=current_day, field=_field, pandas="1")
    # _stock_base = DataAPI.MktStockFactorsDateRangeGet(secID=stock_secIDs, ticker=u"", beginDate=current_day,
    #                                                   endDate=current_day, field=_field, pandas="1")

    # _stock_base["PE"] = _stock_base["PE"].apply(lambda x: 0 if x <= 0 else 5 if x <= 5 else 50 if x >= 50 else x)
    # _stock_base["ROE"] = _stock_base["ROE"].apply(lambda x:
    #                                               0 if x <= 0 else 0.01 if x <= 0.01 else 0.2 if x >= 0.2 else x)

    stock_base = pd.merge(stock_base, _stock_base, how='left', on=['secID', 'tradeDate'])
    stock_base.drop_duplicates(subset="secID", keep="first", inplace=True)
    return stock_base

def load_stock_sector(stock_base):
    # secID have to be in stock_base !
    # 000001 上证综指 399106 深证综指 399001 深证成指
    # 399903 中证100 399905 中证500 000852 中证1000
    # 000300 沪深300 399005 中小100 399008 中小300
    # 000132 上证100 000010 上证180 000009 上证380
    # 399330 深证100 399009 深证200 399007 深证300
    stock_allinone = {
     # "shzs": "000001",  "szzz": "399106",   "szcz": "399001",
    "zz100": "399903", "zz500": "399905", "zz1000": "000852",
    "hs300": "000300", "zx100": "399005",  "zx300": "399008",
    "sh100": "000132", "sh180": "000010",  "sh380": "000009",
    "sz100": "399330", "sz200": "399009",  "sz300": "399007"
    }
    stock_allinone_rt = {k: [] for k, v in stock_allinone.items()}
    stock_allinone_rt_invert = dict()
    for key, val in stock_allinone.items():
        res = DataAPI.IdxConsGet(secID=u"", ticker=val, isNew=u"1", intoDate=u"", field=u"", pandas="1")
        stock_allinone_rt[key] = res.consID.to_dict().values()
    for key, vals in stock_allinone_rt.items():
        for val in vals:
            if val not in stock_allinone_rt_invert:
                stock_allinone_rt_invert[val] = []
            stock_allinone_rt_invert[val].append(key)
    # print(stock_allinone_rt)
    # print(stock_allinone_rt_invert)

    _columns = stock_allinone.keys()
    _res_data = [0 for _ in range(len(_columns))]
    stock_base = dataframe_add_columns(stock_base, _columns, _res_data)
    for key, vals in stock_allinone_rt_invert.items():
        for val in vals:
            stock_base.loc[stock_base["secID"] == key, val] = 1
    # delete *ST stock
    stock_base["toST"] = 0
    stock_base["toST"] = stock_base["secShortName"].apply(lambda x: 1 if ("ST" in x) or ("st" in x) else 0)
    stock_base = stock_base[stock_base["toST"] != 1]
    stock_base = stock_base.drop(["toST"], axis=1)
    # print(stock_base.head())
    return stock_base

def load_sw_industry(stock_base):
    # secID have to be in stock_base !
    stock_secIDs = stock_base.secID.to_dict().values()
    # print (stock_secIDs)
    _field = [
    "secID",  #   str 通联编制的证券编码，可在DataAPI.SecIDGet获取到。
    # "ticker",  #  str 通用交易代码
    # "secShortName",  #    str 证券简称
    "industry",  #    str 行业分类标准
    "industryID",  #  str 行业分类编码，成分记录在最后一级行业分类下，上级行业请查看对应的一二三四级行业编码
    "industrySymbol",  #  str 行业分类编码，行业编制机构发布的行业编码
    "isNew",  #   int 是否最新：1-是，0-否
    "industryID1",  # str 一级行业编码
    "industryName1",  #   str 一级行业
    "industryID2",  # str 二级行业编码
    "industryName2",  #   str 二级行业
    "industryID3",  # str 三级行业编码
    "industryName3",  #   str 三级行业
    ]
    _stock_base = DataAPI.EquIndustryGet(secID=stock_secIDs, ticker=u"", industryVersionCD=u"010303", industry=u"",
                                         industryID=u"", industryID1=u"", industryID2=u"", industryID3=u"",
                                         intoDate=u"", equTypeID=u"", field=_field, pandas="1")
    _stock_base = _stock_base[_stock_base["isNew"] == 1]
    _stock_base = _stock_base.drop(["isNew"], axis=1)
    # print(stock_base.head())
    # print(len(stock_base))
    stock_base = pd.merge(stock_base, _stock_base, how='left', on='secID')
    stock_base.drop_duplicates(subset="secID", keep="first", inplace=True)
    stock_base.dropna(subset=["secID", "industry", "industryID", "industrySymbol"], axis=0, inplace=True)
    # print(stock_base.head())
    # print(len(stock_base))

    sw_groupby_features = [["industryName1"],
                           ["industryName1", "industryName2"],
                           ["industryName1", "industryName2", "industryName3"]]
    for idx, sw_fearures in enumerate(sw_groupby_features):
        _lev = idx + 1
        _lev_names_joint = "sw_lev{}_name_joint".format(_lev)
        stock_base[_lev_names_joint] = stock_base[sw_fearures].apply(lambda x: "_".join(x), axis=1)

    _field_drop = [
    "industry",  #    str 行业分类标准
    "industryID",  #  str 行业分类编码，成分记录在最后一级行业分类下，上级行业请查看对应的一二三四级行业编码
    "industrySymbol",  #  str 行业分类编码，行业编制机构发布的行业编码
    "industryID1",  # str 一级行业编码
    "industryName1",  #   str 一级行业
    "industryID2",  # str 二级行业编码
    "industryName2",  #   str 二级行业
    "industryID3",  # str 三级行业编码
    "industryName3",  #   str 三级行业
    ]
    stock_base = stock_base.drop(_field_drop, axis=1)
    return stock_base
