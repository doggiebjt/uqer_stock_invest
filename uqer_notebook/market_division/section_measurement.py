# 2.1 牛市区间 应用策略逻辑回测
# start = '2005-07-01'                       
start = '2007-01-05' 
end = '2007-10-31'     
# universe = DynamicUniverse(IndSW.JiaYongDianQiL1)        # 证券池，支持股票和基金、期货
universe = StockUniverse('HS300') 
benchmark = 'HS300'                        # 策略参考基准
freq = 'd'                                 # 'd'表示使用日频率回测，'m'表示使用分钟频率回测
refresh_rate = Monthly(1)                  # 执行handle_data的时间间隔
  
# 配置账户信息，支持多资产多账户
accounts = {
    'fantasy_account': AccountConfig(account_type='security', capital_base=10000000)
}
  
def initialize(context):
    pass

def handle_data(context):  # 核心策略逻辑
    current_universe = context.get_universe(exclude_halt=True)
    df_factor = context.history(current_universe, ['PS', 'PCF'], 1, freq='1d', rtype='frame', style='tas')

    yesterday = context.previous_date.strftime('%Y-%m-%d')
    df_factor = df_factor[yesterday]

    # 市销率大于0且低于市场正值平均值
    # 市现率大于0且低于市场正值平均值
    # 管理层持股比例大于市场均值（目前没有这个数据，暂不考虑，若读者有这方面的数据，可以自行上传至Data，进行分析）
    df_factor = df_factor[df_factor['PS'] > 0]
    df_factor = df_factor[df_factor['PCF'] > 0]
    df_factor = df_factor[(df_factor['PS'] < df_factor['PS'].mean())
                          & (df_factor['PCF'] < df_factor['PCF'].mean())]

    # 确定目标仓位
    target_position = list(df_factor.index)

    # 计算权重
    if len(target_position) > 0:
        weight = min(0.1, 1.0 / len(target_position))
    else:
        weight = 0

    account = context.get_account('fantasy_account')
    current_position = account.get_positions(exclude_halt=True)

    # 卖出当前持有，但目标持仓没有的部分
    for stk in set(current_position).difference(target_position):
        account.order_to(stk, 0)

    for stk in target_position:
        account.order_pct_to(stk, weight)
