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

def dataframe_select_drop_cols(t_df, columns, res_data):
    # columns = ["toST"]
    # res_data = [1]
    for _col, _res in zip(columns, res_data):
        t_df = t_df[t_df[_col] == _res]
        t_df = t_df.drop([_col], axis=1)
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
    stock_base = dataframe_add_columns(stock_base, ["shareCapitalRatio"], [0])
    stock_base.shareCapitalRatio = stock_base.nonrestFloatShares / stock_base.totalShares
    stock_base["listDateDelta"] = stock_base["listDate"].apply(lambda x: half_year_transform(n_current_date, x))
    stock_base["tickerPrefixH2"] = stock_base["secID"].apply(lambda x: x[:2])
    return stock_base

def load_base_indicator(stock_base, current_day="20221216"):
    # secID have to be in stock_base !
    # current_day="20221216"
    stock_secIDs = stock_base.secID.to_dict().values()
    # 沪深股票前复权行情
    # _field = [
    #     u'secID', u'tradeDate',
    #     u'preClosePrice', u'openPrice', u'highestPrice', u'lowestPrice', u'closePrice',
    #     u'turnoverVol', u'turnoverValue', u'turnoverRate', u'dealAmount', u'turnoverRate',
    #     u'marketValue', u'negMarketValue', u'accumAdjFactor', u'isOpen'
    # ]
    _field = [
        u'secID', u'tradeDate', u'preClosePrice', u'closePrice',
        u'turnoverVol', u'turnoverValue', u'turnoverRate', u'dealAmount',
        u'marketValue', u'negMarketValue'
    ]
    # 沪深股票前复权行情
    _stock_base = DataAPI.MktEqudAdjGet(secID=stock_secIDs, ticker=u"", tradeDate=current_day,
                                        beginDate=u"", endDate=u"", isOpen=1, field=_field, pandas="1")
    _stock_base.rename(columns={'negMarketValue': "tradeMarketValue"}, inplace=True)
    stock_base = pd.merge(stock_base, _stock_base, how='left', on='secID')
    stock_base.drop_duplicates(subset="secID", keep="first", inplace=True)
    # stock_base["tradeMarketValueCalcu2"] = stock_base["nonrestFloatShares"] * stock_base["closePrice"]
    stock_base["tickerPrefixH3"] = stock_base["secID"].apply(lambda x: x[:3])
    tot_marketValue = stock_base.marketValue.sum()
    tot_tradeMarketValue = stock_base.tradeMarketValue.sum()
    tot_turnoverValue = stock_base.turnoverValue.sum()
    stock_base["totMarketValueProportion"] = stock_base["marketValue"] / tot_marketValue
    stock_base["totTradeMarketValueProportion"] = stock_base["tradeMarketValue"] / tot_tradeMarketValue
    stock_base["totTurnoverValueProportion"] = stock_base["turnoverValue"] / tot_turnoverValue
    stock_base['close_price_rise_rate'] = stock_base['closePrice'] / stock_base['preClosePrice']
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

    sw_groupby_features = [["industryName1"],
                ["industryName1", "industryName2"],
                ["industryName1", "industryName2", "industryName3"]]
    for idx, sw_fearures in enumerate(sw_groupby_features):
        _lev = idx + 1
        _lev_names_joint = "sw_lev{}_name_joint".format(_lev)
        stock_base[_lev_names_joint] = stock_base[sw_fearures].apply(lambda x: "_".join(x), axis=1)

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
        # 价值因子&质量因子
        "CTOP", "CTP5", "ETOP", "ETP5",
        "ROE", "ROE5", "ROA", "ROA5", "PE", "PB", "PCF", "PS",
        "GrossIncomeRatio", "DEGM", "NetProfitRatio", "NetProfitGrowRate", "EGRO",
        # 动量因子&情绪类因子
        "VOL5", "VOL10", "VOL20", "VOL60", "VOL120", "DAVOL5", "DAVOL10", "DAVOL20", "Volatility",  # 换手率相关
        "REVS5", "REVS10", "REVS20",  # 股票的10日收益
        "FiftyTwoWeekHigh",  # 当前价格处于过去1年股价的位置
    ]
    _stock_base = DataAPI.MktStockFactorsOneDayGet(secID=stock_secIDs, ticker=u"",
                                                   tradeDate=current_day, field=_field, pandas="1")
    # _stock_base = DataAPI.MktStockFactorsDateRangeGet(secID=stock_secIDs, ticker=u"", beginDate=current_day,
    #                                                   endDate=current_day, field=_field, pandas="1")

    _stock_base["PE"] = _stock_base["PE"].apply(lambda x: 0 if x <= 0 else 5 if x <= 5 else 50 if x >= 50 else x)
    _stock_base["ROE"] = _stock_base["ROE"].apply(lambda x:
                                                  0 if x <= 0 else 0.01 if x <= 0.01 else 0.2 if x >= 0.2 else x)
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

    # Strategy: 罗伯特•山朋投资理念
    # # 市销率大于0且低于市场正值平均值
    # # 市现率大于0且低于市场正值平均值
    # # 管理层持股比例大于市场均值（无数据此处未加入）
    df_factor = df_factor[df_factor['PS'] > 0]
    df_factor = df_factor[df_factor['PCF'] > 0]
    df_factor = df_factor[(df_factor['PS'] < df_factor['PS'].mean())
                          & (df_factor['PCF'] < df_factor['PCF'].mean())]
    print("罗伯特•山朋: {}".format(len(df_factor)))
    print(df_factor[["secShortName", "industryName1", "industryName2", "industryName3", "tradeMarketValue"]].head(10))
    df_factor_allinone.append(df_factor)
    df_factor = copy.deepcopy(_df_factor[_df_factor[stock_sector] == 1])

    # Strategy: 迈克尔·普莱斯投资理念
    # 筛选条件满足：
    # # 股价与每股净值比小于2
    # # 负债比例低于市场平均值
    # # 公司经营阶层持股越高越好（因没有数据，此处没有加入，有数据的读者可以自行上传测试）
    df_factor = df_factor[df_factor['PB'] < 2]
    df_factor = df_factor[df_factor['DebtsAssetRatio'] < df_factor['DebtsAssetRatio'].mean()]
    print("迈克尔·普莱斯: {}".format(len(df_factor)))
    print(df_factor[["secShortName", "industryName1", "industryName2", "industryName3", "tradeMarketValue"]].head(10))
    df_factor_allinone.append(df_factor)
    df_factor = copy.deepcopy(_df_factor[_df_factor[stock_sector] == 1])

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

    # Strategy: 查尔斯·布兰德投资理念
    # # 年化收益率 -5.4% 基准年化收益率 4.6%
    # # 股票的市盈率不高于市场平均值1.5 倍
    # # 股票的股价/近四季现金流量（市现率）不高于市场平均值的1.5 倍
    # # 股票的市净率不高于市场平均值的1.5 倍
    # # 股票的市净率小于2.0
    # # 股票最近一季负债净值比小于80%
    df_factor = df_factor[df_factor['PB'] > 0]  # addition
    df_factor = df_factor[df_factor['PE'] > 0]  # addition
    df_factor = df_factor[df_factor['PCF'] > 0]  # addition
    df_factor = df_factor[(df_factor['PE'] < 1.0*df_factor['PE'].mean())
                          & (df_factor['PB'] < 1.0*df_factor['PB'].mean())
                          & (df_factor['PCF'] < 1.0*df_factor['PCF'].mean())
                          & (df_factor['PB'] < 2)
                          & (df_factor['DebtEquityRatio'] < 0.8)]
    print("查尔斯·布兰德: {}".format(len(df_factor)))
    print(df_factor[["secShortName", "industryName1", "industryName2", "industryName3", "tradeMarketValue"]].head(10))
    df_factor_allinone.append(df_factor)
    df_factor = copy.deepcopy(_df_factor[_df_factor[stock_sector] == 1])

    return pd.concat(df_factor_allinone)

def calcu_stock_sw_indicator(stock_newest, lev, stock_sw_level_dict, current_date):
    _lev = lev
    _lev_names_joint = "sw_lev{}_name_joint".format(_lev)

    # calcu indicator by sw industry
    tot_marketValue = stock_newest.marketValue.sum()
    tot_tradeMarketValue = stock_newest.tradeMarketValue.sum()
    stock_newest["marketValueProportion"] = stock_newest["marketValue"] / tot_marketValue
    stock_newest["tradeMarketValueProportion"] = stock_newest["tradeMarketValue"] / tot_tradeMarketValue
    # print(stock_newest["marketValueProportion"].sum())
    # print(stock_newest["tradeMarketValueProportion"].sum())
    stock_newest["turnoverRateWeight"] = stock_newest["turnoverRate"] * stock_newest["tradeMarketValueProportion"]
    stock_newest["close_price_rise_rate_weight"] = stock_newest["close_price_rise_rate"] * stock_newest["tradeMarketValueProportion"]
    stock_newest["PE_weight"] = stock_newest["PE"] * stock_newest["tradeMarketValueProportion"]
    stock_newest["ROE_weight"] = stock_newest["ROE"] * stock_newest["tradeMarketValueProportion"]

    feature_rank = 'tradeMarketValue'
    stock_newest['sw_lev{}_tmv_rank_asc'.format(_lev)] = stock_newest.groupby(_lev_names_joint)[feature_rank].rank(ascending = True)
    stock_newest['sw_lev{}_tmv_rank_dsc'.format(_lev)] = stock_newest.groupby(_lev_names_joint)[feature_rank].rank(ascending = False)
    # todo: filter by sw level
    if _lev == 1:
        stock_newest = stock_newest[stock_newest['sw_lev{}_tmv_rank_asc'.format(_lev)] >= 4]
        stock_newest = stock_newest[stock_newest['sw_lev{}_tmv_rank_dsc'.format(_lev)] >= 4]
    if _lev == 2:
        stock_newest = stock_newest[stock_newest['sw_lev{}_tmv_rank_asc'.format(_lev)] >= 2]
        stock_newest = stock_newest[stock_newest['sw_lev{}_tmv_rank_dsc'.format(_lev)] >= 2]
    if _lev == 3:
        stock_newest = stock_newest[stock_newest['sw_lev{}_tmv_rank_asc'.format(_lev)] >= 1]
        stock_newest = stock_newest[stock_newest['sw_lev{}_tmv_rank_dsc'.format(_lev)] >= 1]

    # group by(_lev_names_joint)
    _df_sw_lev_cnt = stock_newest.groupby(_lev_names_joint)["closePrice"].count()

    _df_sw_lev_riseup_rate = stock_newest.groupby(_lev_names_joint)['close_price_rise_rate'].mean()
    _df_sw_lev_trade_turnover_rate = stock_newest.groupby(_lev_names_joint)['turnoverRate'].mean()
    _df_sw_lev_pe = stock_newest.groupby(_lev_names_joint)['PE'].mean()
    _df_sw_lev_roe = stock_newest.groupby(_lev_names_joint)['ROE'].mean()

    _df_sw_lev_riseup_rate_weight = stock_newest.groupby(_lev_names_joint)['close_price_rise_rate_weight'].sum()
    _df_sw_lev_trade_turnover_rate_weight = stock_newest.groupby(_lev_names_joint)['turnoverRateWeight'].sum()
    _df_sw_lev_pe_weight = stock_newest.groupby(_lev_names_joint)['PE_weight'].sum()
    _df_sw_lev_roe_weight = stock_newest.groupby(_lev_names_joint)['ROE_weight'].sum()

    _df_sw_lev_trade_turnover_value = stock_newest.groupby(_lev_names_joint)['turnoverValue'].sum()
    _df_sw_lev_FiftyTwoWeekHigh = stock_newest.groupby(_lev_names_joint)['FiftyTwoWeekHigh'].mean()

    # # stock_newest get_dummies
    # _pd_sw_lev_name = pd.get_dummies(stock_newest[_lev_names_joint], prefix="lev{}_name".format(_lev))
    # stock_newest = pd.concat([stock_newest, _pd_sw_lev_name], axis=1)

    _df_sw_lev_allinone = pd.DataFrame([_df_sw_lev_cnt,  _df_sw_lev_trade_turnover_value, _df_sw_lev_FiftyTwoWeekHigh,
                                        _df_sw_lev_riseup_rate, _df_sw_lev_trade_turnover_rate,
                                        _df_sw_lev_riseup_rate_weight, _df_sw_lev_trade_turnover_rate_weight,
                                        _df_sw_lev_pe, _df_sw_lev_roe, _df_sw_lev_pe_weight, _df_sw_lev_roe_weight]).T
    _df_sw_lev_allinone["tradeDate"] = current_date
    stock_sw_level_dict["sw_lev{}".format(_lev)].append(copy.deepcopy(_df_sw_lev_allinone))  # used for test !
