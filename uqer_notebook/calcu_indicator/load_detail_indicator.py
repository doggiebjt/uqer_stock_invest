# -*- coding: utf-8 -*-
# master strategies 

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
	_stock_base = DataAPI.MktStockFactorsOneDayGet(secID=stock_secIDs, ticker=u"", tradeDate=current_day, field=_field,
												   pandas="1")

	stock_base = pd.merge(stock_base, _stock_base, how='left', on='secID')
	stock_base.drop_duplicates(subset="secID", keep="first", inplace=True)
	return stock_base

def stock_value_investment(_df_factor, stock_sector='ALL', sw_industry='ALL'):
    print("value_invest 0: {}".format(len(_df_factor)))
    df_factor = copy.deepcopy(_df_factor[_df_factor[stock_sector] == 1])
    df_factor = df_factor[df_factor[sw_industry] == 1]
    df_factor_allinone = list()
    print("value_invest 1: {}".format(len(df_factor)))
    
    # Strategy: 柏顿.墨基尔投资理念
    # # 除了购买有题材让投资人脑洞大开的股票之外，我们将这四条简单量化为：
    # # 股票估值PE处于市场最低的20%。
    # # 净利润增长率处于市场最高的20%。
    # # 较长的调仓频率。
    # 筛选条件满足：
    # # 股票估值PE处于市场最低的20%。
    # # 净利润增长率处于市场最高的20%。
    # # 较长的调仓频率。
    df_factor = df_factor[(df_factor['PE'] < df_factor['PE'].quantile(0.2))
                          &(df_factor['NetProfitGrowRate'] > df_factor['NetProfitGrowRate'].quantile(0.8))] 
    print("\n柏顿.墨基尔: {}".format(len(df_factor)))
    print(df_factor[["secShortName", "industryName1", "tradeMarketValue"]])
    df_factor_allinone.append(df_factor)
    df_factor = copy.deepcopy(_df_factor[_df_factor[stock_sector] == 1])

    # Strategy: 格雷厄姆投资理念
    # # 价值 = 当期(正常)利润 × (8.5 + 两倍的预期年增长率)
    # # 因子库中的EGRO因子: 5年收益增长率来代表预期年增长率。
    df_factor['tradeShares'] = df_factor['tradeMarketValue'] / df_factor['closePrice']
    df_factor['masterValue'] = df_factor['tradeShares'] * df_factor['DilutedEPS'] * (10.0 + 5 * df_factor['EGRO'])
    df_factor['masterValue'] = df_factor['masterValue'] - df_factor['tradeMarketValue']
    df_factor = df_factor[df_factor['masterValue'] >= 0]
    print("\n格雷厄姆: {}".format(len(df_factor)))
    print(df_factor[["secShortName", "industryName1", "tradeMarketValue"]])
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
    print("\n罗伯特•山朋: {}".format(len(df_factor)))
    print(df_factor[["secShortName", "industryName1", "tradeMarketValue"]])
    df_factor_allinone.append(df_factor)
    df_factor = copy.deepcopy(_df_factor[_df_factor[stock_sector] == 1])

    # Strategy: 迈克尔·普莱斯投资理念
    # 筛选条件满足：
    # # 股价与每股净值比小于2
    # # 负债比例低于市场平均值
    # # 公司经营阶层持股越高越好（因没有数据，此处没有加入，有数据的读者可以自行上传测试）
    df_factor = df_factor[df_factor['PB'] < 2]
    df_factor = df_factor[df_factor['DebtsAssetRatio'] < df_factor['DebtsAssetRatio'].mean()]
    print("\n迈克尔·普莱斯: {}".format(len(df_factor)))
    print(df_factor[["secShortName", "industryName1", "tradeMarketValue"]])
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
    df_factor = df_factor[(df_factor['PB'] < df_factor['PB'].mean())
                          &(df_factor['PE'] < df_factor['PE'].mean())
                          &(df_factor['PS'] < df_factor['PS'].mean())
                          &(df_factor['LCAP'] < df_factor['LCAP'].mean())
                          &(df_factor['DebtEquityRatio'] < df_factor['DebtEquityRatio'].mean())
                          &(df_factor['ROE5'] > df_factor['ROE5'].mean())
                          &(df_factor['ROA5'] > df_factor['ROA5'].mean())
                          &(df_factor['CTOP'] > df_factor['CTOP'].mean())]
    print("\n惠特尼•乔治: {}".format(len(df_factor)))
    print(df_factor[["secShortName", "industryName1", "tradeMarketValue"]])
    df_factor_allinone.append(df_factor)
    df_factor = copy.deepcopy(_df_factor[_df_factor[stock_sector] == 1])

    # Strategy: 查尔斯·布兰德投资理念
    # # 年化收益率 -5.4% 基准年化收益率 4.6%
    # # 股票的市盈率不高于市场平均值1.5 倍
    # # 股票的股价/近四季现金流量（市现率）不高于市场平均值的1.5 倍
    # # 股票的市净率不高于市场平均值的1.5 倍
    # # 股票的市净率小于2.0
    # # 股票最近一季负债净值比小于80%
    df_factor = df_factor[(df_factor['PE'] < 1.5*df_factor['PE'].mean())  
                          & (df_factor['PB'] < 1.5*df_factor['PB'].mean()) 
                          & (df_factor['PCF'] < 1.5*df_factor['PCF'].mean())
                          & (df_factor['PB'] < 2) 
                          & (df_factor['DebtEquityRatio'] < 0.8)]
    print("\n查尔斯·布兰德: {}".format(len(df_factor)))
    print(df_factor[["secShortName", "industryName1", "tradeMarketValue"]])
    df_factor_allinone.append(df_factor)
    df_factor = copy.deepcopy(_df_factor[_df_factor[stock_sector] == 1])

    return pd.concat(df_factor_allinone)

# if __name__ == "__main__":
stock_newest_random = load_detail_indicator(stock_newest_random, str(n_last_date))  # 增加指标
stock_newest_random = dataframe_add_columns(stock_newest_random, ["ALL"], [1])
stock_newest_random = stock_value_investment(stock_newest_random, stock_sector='zz1000', sw_industry='ALL')
stock_newest_random.drop_duplicates(subset=['secShortName'], keep="first", inplace=True)
print("\n")
print(stock_newest_random)
