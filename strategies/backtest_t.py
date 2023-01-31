## stock trading strategy

## 回测参数初始化设置
start = '2018-03-29'
end   = '2019-03-28'
benchmark = 'HS300'
universe = DynamicUniverse('HS300') # apply_filter方法
capital_base = 10000000
freq = 'd'  # 使用日线回测，每日开盘前执行一次日线策略，仅获得当天的盘前信息。
refresh_rate = 60  # 每60天执行一次handle_data，进行换仓操作。
max_history_window = 60 # 缺省日线数据支持30个交易日

## 账户初始化设置
stock_commission   = Commission(buycost=0.001,sellcost=0.001,unit='perValue')
futures_commission = Commission(buycost=0.001,sellcost=0.001,unit='perValue')
stock_slippage     = Slippage(value=0.0,unit='perValue')
futures_slippage   = Slippage(value=0.0,unit='perValue')

accounts = {
    'stock_account':AccountConfig(account_type = 'security', capital_base= capital_base, commission= stock_commission, slippage= stock_slippage)
}

## 策略初始化环境
def initialize(context):
    pass

## 策略核心算法：按照过去60日收益率排序，选择前60只股票作为买入候选。
def handle_data(context):
    accounts = context.get_account('stock_account')  
    universe = context.get_universe(exclude_halt=True)
    history = context.history(universe,'closePrice',60)

#    print(context.current_date.strftime('%Y-%m-%d')) # FOR TEST !
#    print(len(history.keys()))
#    print(history.keys())
#    print(history['000630.XSHE'])
    
    momentum = {'symbol':[],'c_ret':[]}
    
    for stk in history.keys():
        momentum['symbol'].append(stk)
        momentum['c_ret' ].append(history[stk]['closePrice'][-1] / history[stk]['closePrice'][0])       
#    print(momentum)
    
    momentum = pd.DataFrame(momentum)
#    print(momentum)
    momentum = momentum.sort(columns = 'c_ret',ascending = False).reset_index()
#    print(momentum)
    
    momentum_top60 = momentum[:60]
    buy_list = momentum_top60['symbol'].tolist()
#    print(buy_list)
    
    for stk in accounts.get_positions(): # get_positions方法获得策略当前的所有持仓
        if stk not in buy_list:
            order_to(stk, 0) # 持仓调整（卖出）
            
    portfolio_value = accounts.portfolio_value
    for stk in buy_list:
        order_pct_to(stk, 1.0/len(buy_list)) # 根据当前账户权益按照一定比例下单（买入）
