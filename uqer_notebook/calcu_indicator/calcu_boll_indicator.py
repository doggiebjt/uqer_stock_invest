# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd

import json
import copy
import random
from matplotlib import pyplot as plt


def calcu_boll_indicator(stock_rdate_item):
    stock_rdate_item_factor = dict()
    for secID, _item in stock_rdate_item.items():
        stock_item = copy.deepcopy(_item)
        # # check preClosePrice
        # stock_item["calcu_preClosePrice"] = stock_item.closePrice.shift(1)
        # stock_item["closePriceConsistency"] = stock_item["calcu_preClosePrice"] == stock_item["preClosePrice"]
        # stock_item["closePriceConsistency"] = stock_item["closePriceConsistency"].apply(lambda x: int(x))
        # print(stock_item["closePriceConsistency"].sum(), len(stock_item["closePriceConsistency"]))
        
        stock_item["rectifyPrice"] = stock_item[["openPrice",  "highestPrice",  "lowestPrice",  "closePrice"]].mean(1)  # calcu average price

        # technical indicator
        for _day in [5, 10, 20, 120, 250]:
            stock_item["mean_closePrice_{}days".format(_day)] = stock_item.closePrice.rolling(_day).mean()
            stock_item["variance_closePrice_{}days".format(_day)] = stock_item.closePrice.rolling(_day).std()

        for _day in [5, 10, 20]:
            stock_item["mean_turnoverRate_{}days".format(_day)] = stock_item.turnoverRate.rolling(_day).mean()
            stock_item["variance_turnoverRate_{}days".format(_day)] = stock_item.turnoverRate.rolling(_day).std()

        for _day in [5, 10, 20]:
            stock_item["mean_dealAmount_{}days".format(_day)] = stock_item.dealAmount.rolling(_day).mean()
            stock_item["variance_dealAmount_{}days".format(_day)] = stock_item.dealAmount.rolling(_day).std()

        for _day in [5, 10, 20, 120, 250]:
            stock_item["mean_closePrice_{}days_1x_variance".format(_day)] = stock_item["mean_closePrice_{}days".format(_day)] + stock_item["variance_closePrice_{}days".format(_day)]
            stock_item["mean_closePrice_{}days_2x_variance".format(_day)] = stock_item["mean_closePrice_{}days".format(_day)] + 2 * stock_item["variance_closePrice_{}days".format(_day)]
        
        for _day in [5, 10, 20, 120, 250]:
            calcu_gradient_day = 5
            stock_item["mean_closePrice_{}days_gradient_1x".format(_day)] = stock_item["mean_closePrice_{}days".format(_day)].rolling(calcu_gradient_day).apply(lambda y: np.polyfit(np.arange(len(y)), y, 1)[0])
            stock_item["mean_closePrice_{}days_gradient_2x".format(_day)] = stock_item["mean_closePrice_{}days".format(_day)].rolling(calcu_gradient_day).apply(lambda y: np.polyfit(np.arange(len(y)), y, 2)[0])

        # factors
        for _day in [5, 10, 20, 120, 250]:
            stock_item["select_{}days_factor_1".format(_day)] = stock_item["rectifyPrice"] >= stock_item["mean_closePrice_{}days".format(_day)]
            stock_item["select_{}days_factor_2".format(_day)] = stock_item["rectifyPrice"] >= stock_item["mean_closePrice_{}days_1x_variance".format(_day)]
            stock_item["select_{}days_factor_1".format(_day)] = stock_item["select_{}days_factor_1".format(_day)].apply(lambda x: 0 if int(x) <= 0 else 1) 
            stock_item["select_{}days_factor_2".format(_day)] = stock_item["select_{}days_factor_2".format(_day)].apply(lambda x: 0 if int(x) <= 0 else 1) 
            stock_item["select_{}days_factor_3".format(_day)] = stock_item["mean_closePrice_{}days_gradient_1x".format(_day)].apply(lambda x: 0 if x <= 0 else 1)
            stock_item["select_{}days_factor_4".format(_day)] = stock_item["mean_closePrice_{}days_gradient_2x".format(_day)].apply(lambda x: 0 if x <= 0 else 1)

        # output plot
        for _day in [5, 10, 20, 120, 250]:
            plt.title('plot {} days factor 0'.format(_day))
            stock_item["closePrice"].plot()
            # stock_item["select_{}days_factor_0".format(_day)] = stock_item["select_{}days_factor_1".format(_day)] * stock_item["select_{}days_factor_2".format(_day)] * stock_item["select_{}days_factor_3".format(_day)] * stock_item["select_{}days_factor_4".format(_day)] 
            stock_item["select_{}days_factor_0".format(_day)] = stock_item["select_{}days_factor_3".format(_day)] * stock_item["select_{}days_factor_4".format(_day)] 
            stock_item["select_{}days_factor_0".format(_day)] = stock_item["select_{}days_factor_0".format(_day)] * stock_item["closePrice"].min()
            stock_item["select_{}days_factor_0".format(_day)].plot()
            plt.show()
            plt.title('plot {} days factor 1'.format(_day))
            stock_item["closePrice"].plot()
            stock_item["select_{}days_factor_1".format(_day)] = stock_item["select_{}days_factor_1".format(_day)] * stock_item["closePrice"].min()
            stock_item["select_{}days_factor_1".format(_day)].plot()
            plt.show()
            plt.title('plot {} days factor 2'.format(_day))
            stock_item["closePrice"].plot()
            stock_item["select_{}days_factor_2".format(_day)] = stock_item["select_{}days_factor_2".format(_day)] * stock_item["closePrice"].min()
            stock_item["select_{}days_factor_2".format(_day)].plot()
            plt.show()
            plt.title('plot {} days factor 3'.format(_day))
            stock_item["closePrice"].plot()
            stock_item["mean_closePrice_{}days_gradient_1x".format(_day)].plot()
            stock_item["select_{}days_factor_3".format(_day)] = stock_item["select_{}days_factor_3".format(_day)] * stock_item["closePrice"].min()
            stock_item["select_{}days_factor_3".format(_day)].plot()
            plt.show()
            plt.title('plot {} days factor 4'.format(_day))
            stock_item["closePrice"].plot()
            stock_item["mean_closePrice_{}days_gradient_2x".format(_day)].plot()
            stock_item["select_{}days_factor_4".format(_day)] = stock_item["select_{}days_factor_4".format(_day)] * stock_item["closePrice"].min()
            stock_item["select_{}days_factor_4".format(_day)].plot()
            plt.show()

        stock_rdate_item_factor[secID] = stock_item
        print(stock_item.tail(10))
    return stock_rdate_item_factor

# if __name__ == "__main__":
stock_rdate_item_factor = calcu_boll_indicator(stock_rdate_item)        
