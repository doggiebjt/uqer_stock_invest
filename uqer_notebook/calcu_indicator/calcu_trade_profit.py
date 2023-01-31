# -*- coding: utf-8 -*-

# factor_list = []
# for _day in [5, 10, 20, 120, 250]:
#     for _factor in [0, 1, 2, 3, 4]:
#         factor_list.append("select_{}days_factor_{}".format(_day, _factor))
factor_list = ["select_bull_market_factor_sum_1"]

def parse_trade_behavior(_secID, close_prices, factor_labels, trade_dates, cp_120days_1x_gradient, cp_250days_1x_gradient):
    anchor = 0
    trade_list = []
    for idx in range(len(close_prices) - 1):
        if anchor == 0 and factor_labels[idx] == 0 and factor_labels[idx + 1] > 0:
            trade_list.append([0, 0, 0, 0, 0, 0, 0, 0])  # secID, tradeDate, closePrice, tradeDate, closePrice, profit
            trade_list[-1][0] = _secID
            trade_list[-1][1] = trade_dates[idx + 1]
            trade_list[-1][2] = close_prices[idx + 1]
            anchor = 1
        elif anchor == 1 and factor_labels[idx] > 0 and factor_labels[idx + 1] == 0:
            trade_list[-1][3] = trade_dates[idx + 1]
            trade_list[-1][4] = close_prices[idx + 1]
            trade_list[-1][5] = cp_120days_1x_gradient[idx + 1]
            trade_list[-1][6] = cp_250days_1x_gradient[idx + 1]
            trade_list[-1][7] = (trade_list[-1][4] - trade_list[-1][2]) / trade_list[-1][2]
            anchor = 0
    # print(trade_list)
    return trade_list

def calcu_transaction_profit(stock_rdate_item_factor):
    stock_factor_dict = dict()
    for factor in factor_list:
        stock_factor_dict[factor] = []
    for _secID, _stock_item in stock_rdate_item_factor.items():
        stock_item = copy.deepcopy(_stock_item)
        for factor in factor_list:
            trade_dates = stock_item["tradeDate"]
            close_prices = stock_item["closePrice"]
            cp_120days_1x_gradient = stock_item["mean_closePrice_120days_1x_gradient"]
            cp_250days_1x_gradient = stock_item["mean_closePrice_250days_1x_gradient"]
            factor_labels = stock_item[factor]
            temp_df = parse_trade_behavior(_secID, close_prices, factor_labels, trade_dates, cp_120days_1x_gradient, cp_250days_1x_gradient)
            temp_df = pd.DataFrame(temp_df, columns=["secID", "tradeDate0", "closePrice0", "tradeDate1", "closePrice1", "cp_120days_1x_gradient", "cp_250days_1x_gradient", "profit"])
            stock_factor_dict[factor].append(temp_df)
    return stock_factor_dict

# stock_rdate_item_factor = {'600267.XSHG': stock_rdate_item_factor['600267.XSHG']}
stock_factor_dict = calcu_transaction_profit(stock_rdate_item_factor)

trade_list = []
for factor in stock_factor_dict.keys():
    stock_item = stock_factor_dict[factor]
    for _ in range(len(stock_item)):
        trade_list.append((stock_item[_].secID[0], factor, stock_item[_].profit.sum()))
trade_list = pd.DataFrame(trade_list, columns=["secID", "factor", "profit"])
trade_list.sort_values(by="profit")