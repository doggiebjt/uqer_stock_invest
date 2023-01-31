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

def dataframe_add_columns(t_df, columns, res_data):
    # columns = ["jump_up_date", "jump_dn_date"]
    # res_data = [0, 0]
    for _col, _res in zip(columns, res_data):
        t_df = pd.concat([t_df, pd.DataFrame(columns=list('A'))])
        t_df.rename(columns={'A': _col}, inplace=True)
        t_df[_col] = t_df[_col].apply(lambda x: _res)
    return t_df

def dataframe_select_drop_cols(t_df, columns, res_data):
    # columns = ["toST"]
    # res_data = [1]
    for _col, _res in zip(columns, res_data):
        t_df = t_df[t_df[_col] == _res]
        t_df = t_df.drop([_col], axis=1)
    return t_df

def load_newest_stock():
    # 获取上市股票集合
    _field = [
        # 证券ID # 交易代码 # 证券简称 # 上市板块编码: 1-主板；2-创业板；4-科创板；5-北交所
        u'secID', u'ticker', u'secShortName', u'ListSectorCD',
        # 上市日期 # 总股本(最新)  # 公司无限售流通股份合计(最新)
        u'listDate', 'totalShares', 'nonrestFloatShares'
    ]
    # A-沪深A股 L-上市
    stock_base = DataAPI.EquGet(secID=u"", ticker=u"", equTypeCD=u"A", listStatusCD=u"L", exchangeCD="", ListSectorCD=u"", field=_field,pandas="1")
    # stock_base = dataframe_add_columns(stock_base, ["shareCapitalRatio", "tradeMarketValue"], [0, 0])
    stock_base = dataframe_add_columns(stock_base, ["shareCapitalRatio"], [0])
    stock_base.shareCapitalRatio = stock_base.nonrestFloatShares / stock_base.totalShares
    # print stock_base.head(10)
    return stock_base

def load_base_indicator(stock_base, current_day="20221216"):
    # secID have to be in stock_base !
    # current_day="20221216"
    stock_secIDs = stock_base.secID.to_dict().values()
    # 沪深股票前复权行情
    _field = [
        u'secID', u'tradeDate',
        u'preClosePrice',u'openPrice', u'highestPrice', u'lowestPrice', u'closePrice', 
        u'turnoverVol', u'turnoverValue', u'turnoverRate', u'dealAmount', u'turnoverRate', 
        u'marketValue', u'negMarketValue', u'accumAdjFactor', u'isOpen' 
    ]
    # 沪深股票前复权行情
    _stock_base = DataAPI.MktEqudAdjGet(secID=stock_secIDs, ticker=u"", tradeDate=current_day, beginDate=u"", endDate=u"", isOpen=1, field=_field, pandas="1")
    _stock_base.rename(columns={'negMarketValue': "tradeMarketValue"}, inplace=True)
    stock_base = pd.merge(stock_base, _stock_base, how='left', on='secID')
    stock_base.drop_duplicates(subset="secID", keep="first", inplace=True)
    # stock_base["tradeMarketValue"] = stock_base["nonrestFloatShares"] * stock_base["closePrice"]
    # print (stock_base.head())
    # print (len(stock_base))
    return stock_base

def load_stock_sector(stock_base):
    # secID have to be in stock_base !
    # 000001 上证综指 399106 深证综指 399001 深证成指
    # 399903 中证100 399905 中证500 000852 中证1000
    # 000300 沪深300 399005 中小100 399008 中小300
    # 000132 上证100 000010 上证180 000009 上证380
    # 399330 深证100 399009 深证200 399007 深证300
    stock_allinone = {
     "shzs": "000001",  "szzz": "399106",   "szcz": "399001",
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
    # print stock_allinone_rt
    # print stock_allinone_rt_invert

    _columns = stock_allinone.keys()
    _res_data = [0 for _ in range(len(_columns))]
    stock_base = dataframe_add_columns(stock_base, _columns, _res_data)
    for key, vals in stock_allinone_rt_invert.items():
        for val in vals:
            stock_base.loc[stock_base["secID"] == key, val] = 1
    # delete ST stock
    stock_base = dataframe_add_columns(stock_base, ["toST"], [0])
    stock_base["toST"] = stock_base["secShortName"].apply(lambda x: 1 if "ST" in x  or "st" in x else 0)
    stock_base = stock_base[stock_base["toST"] != 1]
    stock_base = stock_base.drop(["toST"], axis=1)
    # print stock_base.head()
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
    t_stock_base = DataAPI.EquIndustryGet(secID=stock_secIDs, ticker=u"", industryVersionCD=u"010303", industry=u"", industryID=u"", industryID1=u"", industryID2=u"", industryID3=u"", intoDate=u"", equTypeID=u"", field=_field, pandas="1")
    t_stock_base = dataframe_select_drop_cols(t_stock_base, ["isNew"], [1])
    # print stock_base.head()
    # print len(stock_base)
    stock_base = pd.merge(stock_base, t_stock_base, how='left', on='secID')
    stock_base.drop_duplicates(subset="secID", keep="first", inplace=True)
    stock_base.dropna(subset=["secID", "industry", "industryID", "industrySymbol"], axis=0, inplace=True)
    # print (stock_base.head())
    # print (len(stock_base))
    return stock_base

def load_detail_indicator(stock_base, current_day="20221216"):
    # secID have to be in stock_base !
    # current_day = "20221216"
    stock_secIDs = stock_base.secID.to_dict().values()
    # 获取多只股票的因子数据
    _field = [
        "secID", "tradeDate",
        # 价值因子&质量因子
        "CTOP", "CTP5", "ETOP", "ETP5", "ROE", "ROE5", "ROA", "ROA5", "PE", "PB", "PCF", "PS", "EPS", "DilutedEPS",
        "NetProfitRatio", "GrossIncomeRatio", "DEGM", "DebtsAssetRatio", "DebtEquityRatio", "LCAP",
        # 增长类指标
        "NetProfitGrowRate", "NetAssetGrowRate", "TotalProfitGrowRate", "TotalAssetGrowRate",
        "OperatingRevenueGrowRate", "EGRO",
        # 技术指标
        "EMA5", "EMA10", "EMA20", "EMA60", "EMA120", "MA5", "MA10", "MA20", "MA60", "MA120",  # 均线
        "MACD", "KDJ_K", "KDJ_D", "KDJ_J", "BollUp", "BollDown",
        # 动量因子&情绪类因子
        "VOL5", "VOL10", "VOL20", "VOL60", "VOL120", "DAVOL5", "DAVOL10", "DAVOL20", "Volatility",  # 换手率相关
        "REVS5", "REVS10", "REVS20",  # 股票的10日收益
        "FiftyTwoWeekHigh",  # 当前价格处于过去1年股价的位置
        "RSI",  # 相对强弱指标
    ]
    _stock_base = DataAPI.MktStockFactorsOneDayGet(secID=stock_secIDs, ticker=u"", tradeDate=current_day, field=_field, pandas="1")

    stock_base = pd.merge(stock_base, _stock_base, how='left', on='secID')
    stock_base.drop_duplicates(subset="secID", keep="first", inplace=True)
    return stock_base

def stock_value_investment(_df_factor, stock_sector='ALL', sw_industry='ALL'):
    df_factor = copy.deepcopy(_df_factor[_df_factor[stock_sector] == 1])
    df_factor = df_factor[df_factor[sw_industry] == 1]
    df_factor_allinone = list()
    print("value_invest: {}".format(len(df_factor)))
    # Strategy: 柏顿.墨基尔投资理念
    # # 除了购买有题材让投资人脑洞大开的股票之外，我们将这四条简单量化为：
    # # 股票估值PE处于市场最低的20%。
    # # 净利润增长率处于市场最高的20%。
    # # 较长的调仓频率。
    # 筛选条件满足：
    # # 股票估值PE处于市场最低的20%。
    # # 净利润增长率处于市场最高的20%。
    # # 较长的调仓频率。
    df_factor = df_factor[(df_factor['PE'] < df_factor['PE'].quantile(0.25))
                          &(df_factor['NetProfitGrowRate'] > df_factor['NetProfitGrowRate'].quantile(0.75))] 
    print("柏顿.墨基尔: {}".format(len(df_factor)))
    print(df_factor[["secShortName", "industryName1", "industryName2", "industryName3", "tradeMarketValue"]].head(10))
    df_factor_allinone.append(df_factor)
    df_factor = copy.deepcopy(_df_factor[_df_factor[stock_sector] == 1])

    # Strategy: 格雷厄姆投资理念
    # # 价值 = 当期(正常)利润 × (8.5 + 两倍的预期年增长率)
    # # 因子库中的EGRO因子: 5年收益增长率来代表预期年增长率。
    df_factor['tradeShares'] = df_factor['tradeMarketValue'] / df_factor['closePrice']
    df_factor['masterValue'] = df_factor['tradeShares'] * df_factor['DilutedEPS'] * (10.0 + 5 * df_factor['EGRO'])
    df_factor['masterValue'] = df_factor['masterValue'] - df_factor['tradeMarketValue']
    df_factor = df_factor[df_factor['masterValue'] >= 0]
    print("格雷厄姆: {}".format(len(df_factor)))
    print(df_factor[["secShortName", "industryName1", "industryName2", "industryName3", "tradeMarketValue"]].head(10))
    df_factor_allinone.append(df_factor)
    df_factor = copy.deepcopy(_df_factor[_df_factor[stock_sector] == 1])

    # # Strategy: 罗伯特•山朋投资理念
    # # # 市销率大于0且低于市场正值平均值
    # # # 市现率大于0且低于市场正值平均值
    # # # 管理层持股比例大于市场均值（无数据此处未加入）
    # df_factor = df_factor[df_factor['PS'] > 0]
    # df_factor = df_factor[df_factor['PCF'] > 0]
    # df_factor = df_factor[(df_factor['PS'] < df_factor['PS'].mean())  
    #                       & (df_factor['PCF'] < df_factor['PCF'].mean())]
    # print("罗伯特•山朋: {}".format(len(df_factor)))
    # print(df_factor[["secShortName", "industryName1", "industryName2", "industryName3", "tradeMarketValue"]].head(10))
    # df_factor_allinone.append(df_factor)
    # df_factor = copy.deepcopy(_df_factor[_df_factor[stock_sector] == 1])

    # # Strategy: 迈克尔·普莱斯投资理念
    # # 筛选条件满足：
    # # # 股价与每股净值比小于2
    # # # 负债比例低于市场平均值
    # # # 公司经营阶层持股越高越好（因没有数据，此处没有加入，有数据的读者可以自行上传测试）
    # df_factor = df_factor[df_factor['PB'] < 2]
    # df_factor = df_factor[df_factor['DebtsAssetRatio'] < df_factor['DebtsAssetRatio'].mean()]
    # print("迈克尔·普莱斯: {}".format(len(df_factor)))
    # print(df_factor[["secShortName", "industryName1", "industryName2", "industryName3", "tradeMarketValue"]].head(10))
    # df_factor_allinone.append(df_factor)
    # df_factor = copy.deepcopy(_df_factor[_df_factor[stock_sector] == 1])

    # Strategy: 惠特尼•乔治小型价值股投资理念
    # # 筛选条件满足：
    # # 市净率低于全市场平均值 
    # # 最近四季度市盈率小于市场平均值
    # # 最近四季度市销率小于市场平均值 
    # # 总市值小于全市场中位数市值
    # # 现金流市值比(红利)大于市场平均值 
    # # 产权比率（负债总额与所有者权益总额的比率）小于全市场平均值 
    # # 5年权益回报率大于市场平均值 
    # # 5年资产回报率大于市场平均值
    df_factor = df_factor[df_factor['PCF'] > 0]  # addition
    df_factor = df_factor[df_factor['PCF'] < df_factor['PCF'].mean()]  # addition
    df_factor = df_factor[df_factor['PB'] > 0]  # addition
    df_factor = df_factor[df_factor['PE'] > 0]  # addition
    df_factor = df_factor[df_factor['PS'] > 0]  # addition
    df_factor = df_factor[(df_factor['PB'] < df_factor['PB'].mean())
                          &(df_factor['PE'] < df_factor['PE'].mean())
                          &(df_factor['PS'] < df_factor['PS'].mean())
                          &(df_factor['LCAP'] < df_factor['LCAP'].mean())
                          &(df_factor['DebtEquityRatio'] < df_factor['DebtEquityRatio'].mean())
                          &(df_factor['ROE5'] > df_factor['ROE5'].mean())
                          &(df_factor['ROA5'] > df_factor['ROA5'].mean())
                          &(df_factor['CTOP'] > df_factor['CTOP'].mean())]
    print("惠特尼•乔治: {}".format(len(df_factor)))
    print(df_factor[["secShortName", "industryName1", "industryName2", "industryName3", "tradeMarketValue"]].head(10))
    df_factor_allinone.append(df_factor)
    df_factor = copy.deepcopy(_df_factor[_df_factor[stock_sector] == 1])

    # # Strategy: 查尔斯·布兰德投资理念
    # # # 年化收益率 -5.4% 基准年化收益率 4.6%
    # # # 股票的市盈率不高于市场平均值1.5 倍
    # # # 股票的股价/近四季现金流量（市现率）不高于市场平均值的1.5 倍
    # # # 股票的市净率不高于市场平均值的1.5 倍
    # # # 股票的市净率小于2.0
    # # # 股票最近一季负债净值比小于80%
    # df_factor = df_factor[df_factor['PB'] > 0]  # addition
    # df_factor = df_factor[df_factor['PE'] > 0]  # addition
    # df_factor = df_factor[df_factor['PCF'] > 0]  # addition
    # df_factor = df_factor[(df_factor['PE'] < 1.0*df_factor['PE'].mean())  
    #                       & (df_factor['PB'] < 1.0*df_factor['PB'].mean()) 
    #                       & (df_factor['PCF'] < 1.0*df_factor['PCF'].mean())
    #                       & (df_factor['PB'] < 2) 
    #                       & (df_factor['DebtEquityRatio'] < 0.8)]
    # print("查尔斯·布兰德: {}".format(len(df_factor)))
    # print(df_factor[["secShortName", "industryName1", "industryName2", "industryName3", "tradeMarketValue"]].head(10))
    # df_factor_allinone.append(df_factor)
    # df_factor = copy.deepcopy(_df_factor[_df_factor[stock_sector] == 1])

    return pd.concat(df_factor_allinone)


if __name__ == "__main__":
    stock_newest = load_newest_stock()
    stock_newest = load_base_indicator(stock_newest, "20230116")
    stock_newest = load_stock_sector(stock_newest)
    stock_newest = load_sw_industry(stock_newest)
    stock_newest = load_detail_indicator(stock_newest, "20230116")
    print("Load stock done.")
    # for idx in range(50):
    #     print (stock_newest[100*idx: 100*(idx + 1)].to_dict())
