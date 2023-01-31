# -*- coding: utf-8 -*-
# utils by wukesonguo

import numpy as np
import pandas as pd

import json
import copy
import datetime

from matplotlib import pyplot as plt


def half_year_transform(x):
    # print(x)
    s_tradeDate, s_listDate = x
    n_tradeDate = int(s_tradeDate.replace("-", ""))
    n_listDate = int(s_listDate.replace("-", ""))
    d1 = datetime.datetime.strptime(str(n_tradeDate), '%Y%m%d')
    d2 = datetime.datetime.strptime(str(n_listDate), '%Y%m%d')
    delta = d1 - d2
    n_delta = delta.days / 365.0
    return int(n_delta * 10) / 10.0

def calcu_base_indicator(stock_tech_item):
    stock_tech_item['close_price_rise_rate'] = stock_tech_item['closePrice'] / stock_tech_item['preClosePrice']
    stock_tech_item["listDateDeltaDynamic"] = stock_tech_item[["s_tradeDate", "s_listDate"]].apply(lambda x: half_year_transform(x), axis=1)
    stock_tech_item["int_listDateDeltaDynamic"] = stock_tech_item["listDateDeltaDynamic"].apply(lambda x: int(x))
    stock_tech_item['turnoverValue2dealAmountRate'] = stock_tech_item['turnoverValue'] / stock_tech_item['dealAmount']
    stock_tech_item['turnoverRate2dealAmountRate'] = stock_tech_item['turnoverRate'] / stock_tech_item['dealAmount']
    return stock_tech_item


def calcu_close_price_factor(stock_tech_item):
    # 组合均线策略 technical indicators & factors
    # essential: ["openPrice",  "highestPrice",  "lowestPrice",  "closePrice", "turnoverRate", "dealAmount"]

    stock_item = copy.deepcopy(stock_tech_item)
    # stock_item["rectifyPrice"] = stock_item[["openPrice",  "highestPrice",  "lowestPrice",  "closePrice"]].mean(axis=1)  # calcu average price
    # stock_item["closePrice"] = stock_item["rectifyPrice"]

    ma_days = [5, 10, 20, 60, 120, 250]
    # technical indicator
    for _day in ma_days:
        stock_item["mean_closePrice_{}days".format(_day)] = stock_item.closePrice.rolling(_day).mean()
        stock_item["variance_closePrice_{}days".format(_day)] = stock_item.closePrice.rolling(_day).std()

    for _day in ma_days:
        stock_item["mean_turnoverRate_{}days".format(_day)] = stock_item.turnoverRate.rolling(_day).mean()
        stock_item["variance_turnoverRate_{}days".format(_day)] = stock_item.turnoverRate.rolling(_day).std()

    for _day in ma_days:
        stock_item["mean_dealAmount_{}days".format(_day)] = stock_item.dealAmount.rolling(_day).mean()
        stock_item["variance_dealAmount_{}days".format(_day)] = stock_item.dealAmount.rolling(_day).std()

    for _day in ma_days:
        stock_item["mean_closePrice_{}days_1x_variance".format(_day)] = stock_item["mean_closePrice_{}days".format(_day)] + stock_item["variance_closePrice_{}days".format(_day)]
        stock_item["mean_closePrice_{}days_2x_variance".format(_day)] = stock_item["mean_closePrice_{}days".format(_day)] + 2 * stock_item["variance_closePrice_{}days".format(_day)]
    
    calcu_gradient_day = 5
    for _day in ma_days:
        stock_item["mean_closePrice_{}days_1x_gradient".format(_day)] = stock_item["mean_closePrice_{}days".format(_day)].rolling(calcu_gradient_day).apply(lambda y: np.polyfit(np.arange(len(y)), y, 1)[0])
        stock_item["mean_closePrice_{}days_2x_gradient".format(_day)] = stock_item["mean_closePrice_{}days".format(_day)].rolling(calcu_gradient_day).apply(lambda y: np.polyfit(np.arange(len(y)), y, 2)[0])

    stock_item["mean_closePrice_1x_gradient"] = stock_item["closePrice"].rolling(calcu_gradient_day).apply(lambda y: np.polyfit(np.arange(len(y)), y, 1)[0])
    stock_item["mean_closePrice_2x_gradient"] = stock_item["closePrice"].rolling(calcu_gradient_day).apply(lambda y: np.polyfit(np.arange(len(y)), y, 2)[0])

    # factors
    for _day in ma_days:
        # 收盘价站上均线 & 均线Plus方差
        stock_item["select_{}days_0x_variance_factor".format(_day)] = stock_item["closePrice"] >= stock_item["mean_closePrice_{}days".format(_day)]
        stock_item["select_{}days_0x_variance_factor".format(_day)] = stock_item["select_{}days_0x_variance_factor".format(_day)].apply(lambda x: 0 if int(x) <= 0 else 1) 
        stock_item["select_{}days_1x_variance_factor".format(_day)] = stock_item["closePrice"] >= stock_item["mean_closePrice_{}days_1x_variance".format(_day)]
        stock_item["select_{}days_1x_variance_factor".format(_day)] = stock_item["select_{}days_1x_variance_factor".format(_day)].apply(lambda x: 0 if int(x) <= 0 else 1) 
        stock_item["select_{}days_1x_gradient_factor".format(_day)] = stock_item["mean_closePrice_{}days_1x_gradient".format(_day)].apply(lambda x: 0 if x <= 0 else 1)
        stock_item["select_{}days_2x_gradient_factor".format(_day)] = stock_item["mean_closePrice_{}days_2x_gradient".format(_day)].apply(lambda x: 0 if x <= 0 else 1)
    stock_item["select_1x_gradient_factor".format(_day)] = stock_item["mean_closePrice_1x_gradient".format(_day)].apply(lambda x: 0 if x <= 0 else 1)
    stock_item["select_2x_gradient_factor".format(_day)] = stock_item["mean_closePrice_2x_gradient".format(_day)].apply(lambda x: 0 if x <= 0 else 1)

    # factors
    select_bull_market_factor_list = []
    for idx in range(len(ma_days) - 1):
        select_bull_market_factor_list.append("select_bull_market_factor_{}".format(idx))
        stock_item["select_bull_market_factor_{}".format(idx)] = stock_item["mean_closePrice_{}days".format(ma_days[idx+1])] <= stock_item["mean_closePrice_{}days".format(ma_days[idx])]
        stock_item["select_bull_market_factor_{}".format(idx)] = stock_item["select_bull_market_factor_{}".format(idx)].apply(lambda x: 0 if int(x) <= 0 else 1) 
    # stock_item["select_bull_market_factor_0"] = stock_item["select_bull_market_factor_0"].apply(lambda x: 1)  # 是否考虑 cp_ma5 > cp_ma10
    for idx in range(len(ma_days) - 1):
        stock_item["select_bull_market_factor_sum_{}".format(idx)] = stock_item[select_bull_market_factor_list].sum(axis=1)
        stock_item["select_bull_market_factor_sum_{}".format(idx)] = stock_item["select_bull_market_factor_sum_{}".format(idx)].apply(lambda x: x + idx)
        select_bull_market_factor_list.pop()
    # stock_item["select_bull_market_factor"] = stock_item["select_bull_market_factor"].apply(lambda x: 0 if int(x) <= (len(ma_days) - 1) else 1)

    select_bear_market_factor_list = []
    for idx in range(len(ma_days) - 1):
        select_bear_market_factor_list.append("select_bear_market_factor_{}".format(idx))
        stock_item["select_bear_market_factor_{}".format(idx)] = stock_item["mean_closePrice_{}days".format(ma_days[idx+1])] >= stock_item["mean_closePrice_{}days".format(ma_days[idx])]
        stock_item["select_bear_market_factor_{}".format(idx)] = stock_item["select_bear_market_factor_{}".format(idx)].apply(lambda x: 0 if int(x) <= 0 else 1) 
    # stock_item["select_bear_market_factor_0"] = stock_item["select_bear_market_factor_0"].apply(lambda x: 1)  # 是否考虑 cp_ma5 > cp_ma10
    for idx in range(len(ma_days) - 1):
        stock_item["select_bear_market_factor_sum_{}".format(idx)] = stock_item[select_bear_market_factor_list].sum(axis=1)
        stock_item["select_bear_market_factor_sum_{}".format(idx)] = stock_item["select_bear_market_factor_sum_{}".format(idx)].apply(lambda x: x + idx)
        select_bear_market_factor_list.pop()
    # stock_item["select_bear_market_factor"] = stock_item["select_bear_market_factor"].apply(lambda x: 0 if int(x) <= (len(ma_days) - 1) else 1)

    return stock_item

def parse_trade_behavior(_secID, close_prices, factor_labels, trade_dates, cp_120days_1x_gradient, cp_250days_1x_gradient):
    anchor = 0
    trade_list = []
    for idx in range(len(close_prices) - 1):
        if anchor == 0 and factor_labels[idx] == 0 and factor_labels[idx + 1] > 0:
            trade_list.append([0, 0, 0, 0, 0, 0, 0, 0])  # secID, tradeDate, closePrice, tradeDate, closePrice, XX, XX, profit
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

factor_list = ["select_bull_market_factor_sum_1", "select_bear_market_factor_sum_0"]

def calcu_transaction_profit(secID, stock_tech_item):
    _secID = secID
    temp_dfs = []
    stock_item = copy.deepcopy(stock_tech_item)
    stock_item = stock_item.reset_index()
    for factor in factor_list:
        trade_dates = stock_item["s_tradeDate"]
        close_prices = stock_item["closePrice"]
        cp_120days_1x_gradient = stock_item["mean_closePrice_120days_1x_gradient"]
        cp_250days_1x_gradient = stock_item["mean_closePrice_250days_1x_gradient"]
        factor_labels = stock_item[factor]
        temp_df = parse_trade_behavior(_secID, close_prices, factor_labels, trade_dates, cp_120days_1x_gradient, cp_250days_1x_gradient)
        temp_df = pd.DataFrame(temp_df, columns=["secID", "s_tradeDate0", "closePrice0", "s_tradeDate1", "closePrice1", "cp_120days_1x_gradient", "cp_250days_1x_gradient", "profit"])
        if "bull" in factor:
            temp_df["bull_or_bear"] = 1
        if "bear" in factor: 
            temp_df["bull_or_bear"] = -1
        temp_dfs.append(temp_df)
    temp_df_concat = pd.concat(temp_dfs)
    temp_df_concat.sort_values(by=["secID", "s_tradeDate0"], ascending=True, inplace=True)
    return temp_df_concat

def merge_transaction_profit(secID, stock_tech_item):
    merge_profit_result = []
    stock_tech_item["bull_or_bear"] = stock_tech_item["bull_or_bear"].apply(
        lambda x: 2 * x - 1)
    last_row = stock_tech_item.head(1)
    last_row.reset_index(inplace=True)
    last_flag = -last_row["bull_or_bear"][0]
    for row_index, row in stock_tech_item.iterrows():
        row = pd.DataFrame(row).T
        row.reset_index(inplace=True)
        if row["bull_or_bear"][0] != last_flag:
            _row = copy.deepcopy(row)
            if merge_profit_result:
                merge_profit_result[-1]["s_tradeDate1"] = last_row["s_tradeDate1"]
                merge_profit_result[-1]["closePrice1"] = last_row["closePrice1"]
            merge_profit_result.append(_row)
        last_row = copy.deepcopy(row)
        last_flag = last_row["bull_or_bear"][0]

    return pd.concat(merge_profit_result).reset_index()