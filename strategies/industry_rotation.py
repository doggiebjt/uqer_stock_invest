# -*- coding: utf-8 -*-
# https://zhuanlan.zhihu.com/p/34997213

import numpy as np
import pandas as pd
import itertools
import datetime as dt
from datetime import datetime
from dateutil.parser import parse
from scipy import stats as ss
import matplotlib.pyplot as plt
import seaborn as sn

sn.set_style('white')

### 返回申万一级行业历史行情
def get_sw_ind_quotation():
    indus_symbol_raw = DataAPI.IndustryGet(industryVersion="SW",industryVersionCD=u"",industryLevel="1",isNew="1",prntIndustryID=u"",field=u"",pandas="1")['indexSymbol'].tolist() # 获取申万一级行业指数代码
#    print(type(indus_symbol_raw))
#    print(indus_symbol_raw)
    indus_symbol = [str(i) + '.ZICN' for i in indus_symbol_raw]
#    print(type(indus_symbol))
#    print(indus_symbol)

    symbol_history_list = []
    
    for symbol in indus_symbol :
#        print(symbol)
        symbol_history_list_single = DataAPI.MktIdxdGet(indexID=u"",ticker=symbol[:6],tradeDate=u"",beginDate="2015-03-23",endDate="2019-03-22",exchangeCD=u"XSHE,XSHG",field=u"",pandas="1")
#        print(symbol_history_list_single)
        symbol_history_list.append(symbol_history_list_single)
#    print(symbol_history_list[0])
    symbol_history = pd.concat(symbol_history_list, axis=0)  ## WHY !
#    print(symbol_history.shape)
#    print(symbol_history.iloc[0,:])
    symbol_history_unstack = symbol_history.set_index(['tradeDate','ticker']).unstack()['closeIndex'] ## WHY !
#    print(symbol_history_unstack)
    return symbol_history_unstack
    
symbol_history_unstack = get_sw_ind_quotation()  # 获得申万一级行业至今的历史数据
symbol_history_unstack = symbol_history_unstack.iloc[1:,:] # 去除第一期基期
symbol_history_unstack['trade_date'] = symbol_history_unstack.index
# print(symbol_history_unstack)
# print(parse('2015-03-24'))

def get_mon_index(df_index):
    df_index['trade_date'] = df_index['trade_date'].map(lambda x: parse(x))    
    df_index['year_month'] = df_index['trade_date'].map(lambda x: (x.year, x.month)) 
#    print(df_index.groupby(['year_month']).head(1))
    return df_index.groupby(['year_month']).head(1)
    
get_mon_1st_day = get_mon_index(symbol_history_unstack)
get_mon_1st_day = get_mon_1st_day.sort_values(['trade_date'])  # 按trade_date列排序
# print(get_mon_1st_day)

del get_mon_1st_day['trade_date']
del get_mon_1st_day['year_month']
# print(get_mon_1st_day)

get_mon_1st_day_pct = get_mon_1st_day.pct_change(axis = 0)
get_mon_1st_day_pct = get_mon_1st_day_pct.dropna(how ='all')
# print(get_mon_1st_day_pct)
get_mon_1st_day_pct_rank = get_mon_1st_day_pct.rank(axis = 1) # pd.rank()用法
# print(get_mon_1st_day_pct_rank)

indus_sw_raw = DataAPI.IndustryGet(industryVersion="SW",industryVersionCD=u"",industryLevel="1",isNew="1",prntIndustryID=u"",field=u"",pandas="1")
indus_symbol_raw = indus_sw_raw['indexSymbol'].tolist() # 获取申万一级行业指数代码

def get_corr(ind1, ind2, df_ind):
    x = df_ind[ind1].iloc[0:-1].values
    y = df_ind[ind2].iloc[1:  ].values # 计算行业ind1与行业ind2的一阶滞后相关系数
#    print(ind1,ind2)
#    print(np.corrcoef(x,y)[0][1])
    return np.corrcoef(x,y)[0][1]

# get_corr('801010', '801020', get_mon_1st_day_pct_rank)     

predict_corr = {}
for item in itertools.product(indus_symbol_raw, repeat =2):
#    print(item)
    predict_corr[item] = get_corr(item[0],item[1],get_mon_1st_day_pct_rank)

predict_corr = pd.Series(predict_corr)
# print(predict_corr)
predict_corr.hist()

filter_corr = predict_corr[(predict_corr>0.43)|(predict_corr<-0.43)] # 显著性t统计量
filter_corr.sort_values()
print(filter_corr)

filter_corr.index = [(indus_sw_raw[indus_sw_raw['indexSymbol'] == i[0]]['industryName'],indus_sw_raw[indus_sw_raw['indexSymbol'] == i[1]]['industryName']) for i in filter_corr.index]
print(filter_corr)

