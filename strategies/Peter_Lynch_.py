import pandas as pd
import numpy as np
from CAL.PyCAL import *
from pandas import DataFrame, Series
from datetime import datetime, timedelta
import random

#start = '2017-01-01'  # 回测起始时间
#end = '2018-07-30'  # 回测结束时间
#universe = DynamicUniverse('A', exclude_halt=True)   # 证券池 去除停牌股票
cal = Calendar('China.SSE')
span_one = Period('-1B')
span_two = Period('-12M')
span_three = Period('-24M')

today = "2022-12-02"  # today = context.current_date
yesterday = cal.advanceDate(today, span_one)  # "2022-12-01"
next_day = cal.advanceDate(today, span_two)  # "2021-12-02"
pre_day =  cal.advanceDate(today, span_three)  # "2020-12-02"
next_date = cal.adjustDate(next_day, BizDayConvention.Preceding) #前一年剔除非交易日
pre_date = cal.adjustDate(pre_day, BizDayConvention.Preceding)   #前两年剔除非交易日

# _universe = context.get_universe(exclude_halt=True)  # 下面替代此函数
_universe = ["600036", "000333", "000651", "002415", "000004"]  
_universe = DataAPI.SecIDGet(partyID=u"",assetClass=u"E", ticker=_universe, field=['secID'], pandas="1")
_universe = list(_universe['secID'])

_universe = DataAPI.EquGet(secID=u"",ticker=u"",equTypeCD=u"A",
                           listStatusCD=u"L",exchangeCD="",ListSectorCD=u"",field=['secID'],pandas="1")
_universe = (list(_universe['secID']))
random.shuffle(_universe)
_universe = _universe[:1000]

# method-1 去除ST股 某日被标为ST
df_ST = DataAPI.SecSTGet(secID=_universe, beginDate=today, endDate=today, field=['secID']) 
_universe = [s for s in _universe if s not in list(df_ST['secID'])]

# # method-2 暴力去掉名字里含有 ST 等字样的股票
# df_ST = DataAPI.EquGet(secID=_universe,field=u"secID,secShortName", pandas="1")
# print(df_ST)
# STlist = list(df_ST.loc[df_ST.secShortName.str.contains('S'), 'secID'])
# _universe = [s for s in _universe if s not in STlist]  
# # ['000333.XSHE', '000651.XSHE', '002415.XSHE', '600036.XSHG']

# 去除 n_days 内上市的新股
tradeDate= today
day = 30
ticker = _universe
tradeDate = tradeDate if tradeDate is not None else datetime.now().strftime('%Y%m%d')
period = '-' + str(day) + 'B'
pastDate = cal.advanceDate(tradeDate,period)  # 交易日期的30天
pastDate = pastDate.strftime("%Y-%m-%d")

tickerDist={}
tickerShort=[] 
for index in range(len(ticker)):
    OneTickerShort=ticker[index][0:6]
    tickerShort.append(OneTickerShort)
    tickerDist[OneTickerShort]=ticker[index]
print tickerDist
ipo_date = DataAPI.SecIDGet(partyID=u"",assetClass=u"E",ticker=tickerShort,cnSpell=u"",field=u"ticker,listDate",pandas="1")
print ipo_date
remove_list = ipo_date[ipo_date['listDate'] > pastDate]['ticker'].tolist()
remove_list=[values for keys,values in tickerDist.items() if keys in remove_list ]
_universe = [stk for stk in ticker if stk not in remove_list]

# PEG_count 获取股票 list
univ = _universe
tradedate_start = yesterday
tradedate_end = next_date
tradedate_pre = pre_date

filename1='OperatingRevenueGrowRate'  #营收增长率
filename2='EPS'                       #每股收益
filename3='PE'                        #市盈率
filename4='preClosePrice'             #市价
filename5='inventories'               #存货

print univ
print tradeDate
print tradedate_start
print tradedate_end
print tradedate_pre
print "##########"

# 第一步筛选：选取市盈率ttm>0,且彼得林奇因子>0.5的公司
# 计算12个月的 eps 增长率
EPS1=DataAPI.MktStockFactorsOneDayGet(tradeDate=tradedate_end, secID=univ, field=['secID', filename2], pandas='1').dropna().set_index('secID') # 每股收益 
EPS1.rename(columns={'EPS':'old'},inplace=True)
EPS2=DataAPI.MktStockFactorsOneDayGet(tradeDate=tradedate_start, secID=univ, field=['secID', filename2], pandas='1').dropna().set_index('secID') # 每股收益 
EPS2.rename(columns={'EPS':'new'},inplace=True)

EPS = EPS1.merge(EPS2,how='outer', left_index=True,right_index=True)
EPS = pd.concat([EPS, pd.DataFrame(columns=list('D'))])
EPS.rename(columns={'D':'EPSgrowth'},inplace=True)

EPS['EPSgrowth'] = (EPS['new']/EPS['old'])-1
#EPS = EPS[EPS['EPSgrowth']>0]
EPS = EPS.sort(columns = 'EPSgrowth',ascending=False)
EPS = EPS.drop(['new','old'],axis=1)  #未处理的EPS增长率列表（乘100）
print EPS

# 计算股息率 此指标存在问题！ 格力电器一年内分红两次接口仅返回一次分红结果
factor3 = DataAPI.EquDivGet(eventProcessCD='6',secID= univ ,beginDate=tradedate_end ,endDate=tradedate_start ,field=['secID','perCashDiv','recordDate'],pandas="1").dropna() 
factor3 = factor3.sort('recordDate',ascending=False).drop_duplicates('secID') 
factor3.set_index('secID',inplace=True)

factor4  = pd.concat([factor3, pd.DataFrame(columns=list('D'))])
for s in list(factor3.index) :     
    factor5 = DataAPI.MktEqudGet(secID = s, tradeDate= factor3['recordDate'][s],field=['secID','closePrice'],pandas="1")
    factor5.set_index('secID',inplace=True)
    factor4.loc[s,'D'] = factor5.values
for s in range(0,len(factor4['D'])):
    i = factor4['D'][s]
    if i == []:
        i = 1
        factor4['recordDate'][s]=0
    else:
        i = i[0]
        factor4['D'][s] = i
        factor4['recordDate'][s] = factor4['perCashDiv'][s]/factor4['D'][s]*100
factor4.rename(columns={'recordDate':'gxl'},inplace=True)
factor4.rename(columns={'D':'closePrice'},inplace=True)
gxl = factor4.drop(['closePrice','perCashDiv'],axis=1) 
print gxl.head(20)

# 计算市盈率TTM    
_tradedate_start=str(tradedate_start).replace("-", "")  # notice !
pe = DataAPI.MktEqudGet(secID=univ, tradeDate=_tradedate_start, field=['secID', 'PE'], pandas="1").dropna().set_index('secID')
print pe.head(20)
PL = pd.merge(EPS,gxl,how='outer', left_index=True,right_index=True)
PL = pd.merge(PL,pe,how='outer', left_index=True,right_index=True)

# 计算彼得林奇因子
PL = pd.concat([PL, pd.DataFrame(columns=list('D'))])
PL.rename(columns={'D':'PL'},inplace=True)
print PL.head(20)

PL['PL'] = (PL['EPSgrowth']+PL['gxl'])/PL['PE']
PL = PL.drop(['EPSgrowth','gxl','PE'],axis=1)
term1 = PL.dropna()       
#term1 = PL[PL['PL']>0.5]    

print term1.head(20)

# 营业增长率
filename1 = 'OperatingRevenueGrowRate'
yyzzl = DataAPI.MktStockFactorsOneDayGet(tradeDate=tradedate_end, secID=univ, field=['secID',filename1], pandas='1').dropna().set_index('secID')      
yyzzl[filename1] = (yyzzl[filename1])*100

print yyzzl.head(20)

# 计算存货增长率
filename5='inventories'  #存货
chnew = DataAPI.FdmtBSAllLatestGet(secID=univ,reportType='A',endDate=tradedate_start,beginDate=tradedate_end,field=['secID',filename5,],pandas="1").dropna().set_index('secID')     #新存货

chnew.rename(columns={'inventories':'new'},inplace=True)
chold = DataAPI.FdmtBSAllLatestGet(secID=univ,reportType='A',endDate=tradedate_end,beginDate=tradedate_pre,field=['secID',filename5,],pandas="1").dropna().set_index('secID')       #旧存货
chold.rename(columns={'inventories':'old'},inplace=True)

ch = chnew.merge(chold,how='outer', left_index=True,right_index=True)
ch = pd.concat([ch, pd.DataFrame(columns=list('D'))])
ch.rename(columns={'D':'chgrowth'},inplace=True)
#ch['chgrowth'] = ((ch['new']/ch['old'])-1)*100

# 防火防盗防零值
for i in list(ch.index) :
    try:
        # ((ch['new'][i]/ch['old'][i])-1)*100
        ch['chgrowth'][i] = ((ch['new'][i]/ch['old'][i])-1)*100 
    except ZeroDivisionError, e:
            ch['chgrowth'][i] = 0

ch = ch.drop(['new','old'],axis=1)                                     #未处理的存货增长率(乘100)

term2 = pd.merge(yyzzl,ch,how='outer', left_index=True,right_index=True)
#term2 = term2[term2['OperatingRevenueGrowRate']>term2['chgrowth']]    #获取营业增长率与存货增长率

print  term2.head(20)

_tradedate_start=str(tradedate_start).replace("-", "")  # notice !
pe = DataAPI.MktEqudGet(secID=univ,tradeDate=_tradedate_start,field=['secID',filename3],pandas="1").dropna().set_index('secID')             #市盈率
term3 = pe
term3 = pe[pe['PE']>0]    

buylist = pd.merge(term1,term2,how='outer', left_index=True,right_index=True)
buylist = pd.merge(buylist,term3,how='outer', left_index=True,right_index=True)
# print buylist.head(20)
buylist = buylist[buylist['PL']>0.5]                                       #条件一：PL大于0.5
# buylist = buylist[buylist['OperatingRevenueGrowRate']>buylist['chgrowth']] #条件二：营增大于存增
num = int(len(buylist)*0.66)
buylist = buylist.sort(columns = 'PE',ascending=True).head(num)           #条件三：PE大于0且属于后2/3
print buylist
#print buylist
buylist_index = list(buylist.index)

print buylist_index
