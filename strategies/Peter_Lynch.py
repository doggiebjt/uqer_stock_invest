import pandas as pd
import numpy as np
from CAL.PyCAL import *
from pandas import DataFrame, Series
from datetime import datetime, timedelta

# 第一步筛选：选取市盈率ttm > 0,且彼得林奇因子 > 0.5的公司
# 第二步筛选：
# 1.选取存货同比增长率小于营收增长理财的公司，选取市盈率出去后2/3;
# 2.快速增长型公司：选取营收同比增长大于0且营收同比增长率及净利润同比增长率小于50%的公司
# 3.稳定增长型公司：选取市盈率（TTM）大于0，且市盈率处于后2/3的公司。

#父子类函数封装
from functools import wraps
def wrapper_func_cache(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        if not hasattr(func, '__cache_result'):
            func.__cache_result = {}
        
        hash_key = [str(i) for i in args] + [str(j) for j in kwargs.iteritems()]
        cache_key = hash(tuple(hash_key))
        
        if cache_key not in func.__cache_result:
            func.__cache_result[cache_key] = func(*args, **kwargs)
            
        return func.__cache_result[cache_key]
    return wrapped

def st_remove(source_universe, st_date=None):
    """
    给定股票列表,去除其中在某日被标为ST的股票
    Args:
        source_universe (list of str): 需要进行筛选的股票列表
        st_date (datetime): 进行筛选的日期,默认为调用当天
    Returns:
        list: 去掉ST股票之后的股票列表

    Examples:
        >> universe = set_universe('A')
        >> universe_without_st = st_remove(universe)
    """
    st_date = st_date if st_date is not None else datetime.now().strftime('%Y%m%d')
    df_ST = DataAPI.SecSTGet(secID=source_universe, beginDate=st_date, endDate=st_date, field=['secID'])
    return [s for s in source_universe if s not in list(df_ST['secID'])]

def new_remove(ticker,tradeDate= None,day = 30):
    tradeDate = tradeDate if tradeDate is not None else datetime.now().strftime('%Y%m%d')
    period = '-' + str(day) + 'B'
    pastDate = cal.advanceDate(tradeDate,period)
    pastDate = pastDate.strftime("%Y-%m-%d")

    tickerDist={}
    tickerShort=[] 
    for index in range(len(ticker)):
        OneTickerShort=ticker[index][0:6]
        tickerShort.append(OneTickerShort)
        tickerDist[OneTickerShort]=ticker[index]

    ipo_date = DataAPI.SecIDGet(partyID=u"",assetClass=u"",ticker=tickerShort,cnSpell=u"",field=u"ticker,listDate",pandas="1")
    remove_list = ipo_date[ipo_date['listDate'] > pastDate]['ticker'].tolist()
    remove_list=[values for keys,values in tickerDist.items() if keys in remove_list ]
    return [stk for stk in ticker if stk not in remove_list] 

def univClear(_universe, context, today):
    # 1. 去除停牌股票
    univ = _universe

    # 2. 去除ST股
    df_ST = DataAPI.SecSTGet(secID=univ, beginDate=today, endDate=today, field=['secID']) 
    univ = [s for s in univ if s not in list(df_ST['secID'])]
    
    # 下面这种方法是暴力去掉名字里含有 ST 等字样的股票
    df_ST = DataAPI.EquGet(secID=univ,field=u"secID,secShortName",pandas="1")
    STlist = list(df_ST.loc[df_ST.secShortName.str.contains('S'), 'secID'])
    univ = [s for s in univ if s not in STlist]
    return univ

#计算PEG因子
def PEG_count(univ,tradedate_start,tradedate_end,tradedate_pre):
    
    filename1='OperatingRevenueGrowRate'  #营收增长率
    filename2='EPS'                       #每股收益
    filename3='PE'                        #市盈率
    filename4='preClosePrice'             #市价
    filename5='inventories'               #存货

    #计算12个月的eps增长率
    EPS1=DataAPI.MktStockFactorsOneDayGet(tradeDate=tradedate_end, secID=univ, field=['secID',filename2], pandas='1').dropna().set_index('secID') # 每股收益 
    EPS1.rename(columns={'EPS':'old'},inplace=True)
    EPS2=DataAPI.MktStockFactorsOneDayGet(tradeDate=tradedate_start, secID=univ, field=['secID',filename2], pandas='1').dropna().set_index('secID') # 每股收益 
    EPS2.rename(columns={'EPS':'new'},inplace=True)

    EPS = EPS1.merge(EPS2,how='outer', left_index=True,right_index=True)
#EPS=EPS[EPS[filename3]>0]
#EPS=EPS.sort(columns = filename3).head(num)
    EPS = pd.concat([EPS, pd.DataFrame(columns=list('D'))])
    EPS.rename(columns={'D':'EPSgrowth'},inplace=True)

    EPS['EPSgrowth'] = (EPS['new']/EPS['old'])-1
#EPS = EPS[EPS['EPSgrowth']>0]
    EPS = EPS.sort(columns = 'EPSgrowth',ascending=False)
    EPS = EPS.drop(['new','old'],axis=1)                        #未处理的EPS增长率列表（乘100）
    
    #计算股息
    factor3 = DataAPI.EquDivGet(eventProcessCD = '6',secID= univ ,beginDate = tradedate_end ,endDate= tradedate_start ,field=['secID','perCashDiv','recordDate'],pandas="1").dropna() 
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
                                                                  
   #计算市盈率TTM                                                      
    pe = DataAPI.MktEqudGet(secID=univ,tradeDate=tradedate_start,field=['secID',filename3],pandas="1").dropna().set_index('secID')
    PL = pd.merge(EPS,gxl,how='outer', left_index=True,right_index=True)
    PL = pd.merge(PL,pe,how='outer', left_index=True,right_index=True)
    PL = pd.concat([PL, pd.DataFrame(columns=list('D'))])
    PL.rename(columns={'D':'PL'},inplace=True)
   
    #获取彼得林奇因子
    PL['PL'] = (PL['EPSgrowth']+PL['gxl'])/PL['PE']
    PL = PL.drop(['EPSgrowth','gxl','PE'],axis=1)
    term1 = PL.dropna()       
#term1 = PL[PL['PL']>0.5]                                                                    

     #营业增长率
    yyzzl = DataAPI.MktStockFactorsOneDayGet(tradeDate=tradedate_end, secID=univ, field=['secID',filename1], pandas='1').dropna().set_index('secID')      
    yyzzl[filename1] = (yyzzl[filename1])*100

    #存货增长率
    chnew = DataAPI.FdmtBSAllLatestGet(secID=univ,reportType='A',endDate=tradedate_start,beginDate=tradedate_end,field=['secID',filename5,],pandas="1").dropna().set_index('secID')     #新存货

    chnew.rename(columns={'inventories':'new'},inplace=True)
    chold = DataAPI.FdmtBSAllLatestGet(secID=univ,reportType='A',endDate=tradedate_end,beginDate=tradedate_pre,field=['secID',filename5,],pandas="1").dropna().set_index('secID')       #旧存货
    chold.rename(columns={'inventories':'old'},inplace=True)

    ch = chnew.merge(chold,how='outer', left_index=True,right_index=True)
    ch = pd.concat([ch, pd.DataFrame(columns=list('D'))])
    ch.rename(columns={'D':'chgrowth'},inplace=True)
#ch['chgrowth'] = ((ch['new']/ch['old'])-1)*100
#防火防盗防零值
    for i in list(ch.index) :
        try:
            ((ch['new'][i]/ch['old'][i])-1)*100
            ch['chgrowth'][i] = ((ch['new'][i]/ch['old'][i])-1)*100 
        except ZeroDivisionError, e:
             ch['chgrowth'][i] = 0
    #else:ch['chgrowth'][i] = ((ch['new'][i]/ch['old'][i])-1)*100 

#ch = ch[ch['chgrowth']>0] 

#ch = ch[ch['chgrowth']>0]
#ch = ch.sort(columns = 'chgrowth',ascending=False)
    ch = ch.drop(['new','old'],axis=1)                                     #未处理的存货增长率(乘100)
    term2 = pd.merge(yyzzl,ch,how='outer', left_index=True,right_index=True)
#term2 = term2[term2['OperatingRevenueGrowRate']>term2['chgrowth']]    #获取营业增长率与存货增长率

    pe = DataAPI.MktEqudGet(secID=univ,tradeDate=tradedate_start,field=['secID',filename3],pandas="1").dropna().set_index('secID')             #市盈率
    term3 = pe
#term3 = pe[pe['PE']>0]                                                     #获取PE

    buylist = pd.merge(term1,term2,how='outer', left_index=True,right_index=True)
    buylist = pd.merge(buylist,term3,how='outer', left_index=True,right_index=True)
    buylist = buylist[buylist['PL']>0.5]                                       #条件一：PL大于0.5
    buylist = buylist[buylist['OperatingRevenueGrowRate']>buylist['chgrowth']] #条件二：营增大于存增
    num = int(len(buylist)*0.66)
    buylist = buylist.sort(columns = 'PE',ascending=True).head(num)           #条件三：PE大于0且属于后2/3
#print buylist
    buylist_index = list(buylist.index)
    return buylist_index


#回测代码
start = '2017-01-01'                       # 回测起始时间
end = '2018-07-30'                         # 回测结束时间
universe = DynamicUniverse('A')            # 证券池
benchmark = 'ZZ500'                        # 策略参考标准
freq = 'd'                                 # 策略类型，'d'表示日间策略使用日线回测，'m'表示日内策略使用分钟线回测
refresh_rate = Monthly(1)                           # 调仓频率，表示执行handle_data的时间间隔，若freq = 'd'时间间隔的单位为交易日，若freq = 'm'时间间隔为分钟
cal = Calendar('China.SSE')
span_one = Period('-1B')
span_two = Period('-12M')
span_three = Period('-24M')
 
# 配置账户信息，支持多资产多账户
accounts = {
    'stock_account': AccountConfig(account_type='security', capital_base=10000000, commission = Commission(buycost=0.0005, sellcost=0.0015, unit='perValue'), slippage = Slippage(value=0.00, unit='perShare'))
}

def initialize(context):
    pass
  
# 每个单位时间(如果按天回测,则每天调用一次,如果按分钟,则每分钟调用一次)调用一次
def handle_data(context):    
    today = context.current_date #将原本的today替换成账户日期,preday,nextday同理
    yesterday = cal.advanceDate(today, span_one)
    next_day = cal.advanceDate(today, span_two)
    pre_day =  cal.advanceDate(today, span_three)
    next_date = cal.adjustDate(next_day, BizDayConvention.Preceding) #前一年剔除非交易日
    pre_date = cal.adjustDate(pre_day, BizDayConvention.Preceding)   #前两年剔除非交易日
    _universe = context.get_universe(exclude_halt=True)
    _universe = univClear(_universe, context, today)
    _universe = new_remove(_universe)
    _universe = st_remove(_universe)
    
    buy_list = PEG_count(_universe, yesterday, next_date, pre_date) #获取股票list 

    # 获取当前账户信息
    account = context.get_account('stock_account')   
    current_position = account.get_positions(exclude_halt=True)       
     
    # 卖出当前持有，但目标持仓没有的部分
    for stock in set(current_position).difference(buy_list):
        account.order_to(stock, 0)
     
    # 根据目标持仓权重，逐一委托下单
    for stock in buy_list:
        account.order_pct_to(stock, 1./len(buy_list))