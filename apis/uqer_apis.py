# -*- coding: utf-8 -*-
# 获取全部申万一级分类
_field = [
    u"industryID", u"industryName"
]
res = DataAPI.IndustryGet(industryVersion=u"", industryVersionCD=u"010303", industryLevel=["1"], isNew=u"1", prntIndustryID=u"", industryName=u"", industryID=u"", field=_field, pandas="1")

# 获取上市股票集合
_field = [
    u'secID', u'ticker', u'secShortName', u'listDate', u'consExchangeCD'
]
stock_sh = DataAPI.SecIDGet(partyID=u"", ticker=u"", cnSpell=u"", assetClass=u"E", exchangeCD="XSHG", listStatusCD="L", field=_field, pandas="1")
stock_sz = DataAPI.SecIDGet(partyID=u"", ticker=u"", cnSpell=u"", assetClass=u"E", exchangeCD="XSHE", listStatusCD="L", field=_field, pandas="1")

# 000001 上证综指 399106 深证综指 399001 深证成指
# 399903 中证100 399905 中证500 000852 中证1000
# 000300 沪深300 399005 中小100 399008 中小300
# 000132 上证100 000010 上证180 000009 上证380
# 399330 深证100 399009 深证200 399007 深证300
res = DataAPI.IdxConsGet(secID=u"", ticker=u"399001", isNew=u"1", intoDate=u"", field=u"", pandas="1")
secIDS = res.consID.to_dict().values()

# 获取股票行业分类
res = DataAPI.EquIndustryGet(secID=u"",ticker=["000333","000651"],industryVersionCD=u"010303",industry=u"",industryID=u"",industryID1=u"",industryID2=u"",industryID3=u"",intoDate=u"",equTypeID=u"",field=["secID", "ticker", "secShortName", "secFullName", "isNew", "industryID1", "industryName1", "industryID2", "industryName2", "equType"],pandas="1")
res = res[res["isNew"] == 1]
res = res.drop(labels=["isNew"], axis=1)
print res.head(10)

res = DataAPI.IndustryGet(industryVersion=u"",industryVersionCD=u"010303",industryLevel=["1"],isNew=u"1",prntIndustryID=u"",industryName="",industryID=u"",field=["industryID", "industryName"],pandas="1")
print res.head(10)

# 股票基本信息
_field = [u'secID', u'ticker', u'exchangeCD', u'ListSector', 
          u'secShortName', u'secFullName', u'equType', 
          u'totalShares', u'nonrestFloatShares', u'nonrestfloatA', u'TShEquity']
res = DataAPI.EquGet(secID=u"000333.XSHE", ticker=u"", equTypeCD=u"A", listStatusCD=u"L", exchangeCD="", ListSectorCD=u"", field=_field, pandas="1")
print res.head(10)

# 沪深股票前复权行情
current_day = str(current_day).replace("-", "")
_field = [
    u'secID', u'ticker', u'secShortName', u'exchangeCD', u'tradeDate',
    u'preClosePrice', u'actPreClosePrice', u'openPrice', u'highestPrice',
    u'lowestPrice', u'closePrice', u'turnoverVol', u'negMarketValue',
    u'dealAmount', u'turnoverRate', u'accumAdjFactor', u'turnoverValue',
    u'marketValue', u'chgPct', u'PE', u'PB', u'isOpen', u'vwap'
]
res = DataAPI.MktEqudAdjGet(secID=u"", ticker=u"000333", tradeDate=current_day, beginDate=u"", endDate=u"", isOpen="", field=_field, pandas="1")
print res.head(10)

# 沪深股票日行情
one_year_day = str(one_year_day).replace("-", "")
res_t = DataAPI.MktEqudGet(secID=u"", ticker=u"000333", tradeDate=u"", beginDate=two_year_day, endDate=current_day, isOpen="", field=_field, pandas="1")
print res_t.head(10)

res_t.pivot_table(index='tradeDate',columns='secID',values='closePrice')

# 获取多只股票的因子数据
_field = [
    "secID", "ticker", "tradeDate", 
    # 价值因子&质量因子
    "CTOP", "CTP5", "ETOP", "ETP5", "ROE", "ROE5", "ROA", "ROA5", "PE", "PB", "PCF", "PS", "NetProfitRatio", "GrossIncomeRatio", "DEGM",
    # 增长类指标
    "NetProfitGrowRate", "NetAssetGrowRate", "TotalProfitGrowRate", "TotalAssetGrowRate", "OperatingRevenueGrowRate", "EGRO",
    # 技术指标
    "EMA5", "EMA10", "EMA20", "EMA60", "EMA120", "MA5", "MA10", "MA20", "MA60", "MA120", 
    # 动量因子&情绪类因子
    "VOL5", "VOL10", "VOL20", "DAVOL5", "DAVOL10", "DAVOL20", "REVS5", "REVS10", "REVS20", "RSI" 
]
res = DataAPI.MktStockFactorsOneDayGet(secID=u"", ticker=u"000333", tradeDate=current_day, field=_field, pandas="1")
print res.head(10)
res = DataAPI.MktStockFactorsDateRangeGet(secID=u"", ticker=u"000333", beginDate=current_day, endDate=current_day, field=_field, pandas="1")
print res.head(10)

_field = [
    'secID','tradeDate','ROE'
]
df_roe = DataAPI.MktStockFactorsOneDayGet(tradeDate="20221208", secID=set_universe('A'), field=_field, pandas="1")
print(df_roe)
df_roe['ROE'].plot.hist(bins = 100) # 直方图绘制
# df_roe.boxplot(sym='rs') # 箱体图绘制
# 野值剔除
df_roe.loc[df_roe.ROE-df_roe.ROE.mean() < -3.0 * df_roe.ROE.std(), 'ROE'] = df_roe.ROE.mean() - 3 * df_roe.ROE.std()
df_roe.loc[df_roe.ROE-df_roe.ROE.mean() > +3.0 * df_roe.ROE.std(), 'ROE'] = df_roe.ROE.mean() + 3 * df_roe.ROE.std()
df_roe['ROE'].plot.hist(bins = 100) 
