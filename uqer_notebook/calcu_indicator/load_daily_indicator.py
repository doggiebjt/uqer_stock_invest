# -*- coding: utf-8 -*-

def read_stock_base_read(stock_rdate_item):
    for _secID in stock_newest_random.secID:
        # 沪深股票前复权行情
        _field = [
            u'secID', u'ticker', u'secShortName', u'tradeDate',
            u'openPrice', u'highestPrice', u'lowestPrice', u'closePrice', u'preClosePrice',
            u'negMarketValue', u'marketValue', u'turnoverRate', u'turnoverValue', u'dealAmount',
            u'accumAdjFactor', u'isOpen', u'vwap'
        ]
        res = DataAPI.MktEqudAdjGet(secID=_secID, ticker=u"", tradeDate="", beginDate=s_ten_year_date, endDate=s_last_date,  # s_ten_year_date
                                    isOpen="1", field=_field, pandas="1")
        res = res[res["isOpen"] == 1]
        res["n_date"] = res["tradeDate"].apply(lambda x: int(x.replace("-", "")))
        res.rename(columns={'negMarketValue': "tradeMarketValue"}, inplace=True)
        res["tradePercent"] = res["tradeMarketValue"] / res["marketValue"]
        res.drop(["isOpen", "vwap", "accumAdjFactor"], axis=1, inplace="True")
        
        # _dealAmount = copy.deepcopy(res["dealAmount"])
        # # res.drop(["dealAmount"], axis=1, inplace="True")
        # _dealAmount = _dealAmount.fillna(0)
        # res["dealAmountAdj"] = _dealAmount / res["tradeMarketValue"]
        
        # print("dropna 0: {}".format(len(res)))
        # res.dropna(axis=0, how='any', thresh=None, subset=None, inplace=True)
        # print("dropna 1: {}".format(len(res)))
        
        stock_rdate_item[_secID] = res

    # # plot stock close_price curve
    # for key, val in stock_rdate_item.items():
    #     print(val["tradeDate"].head(1))
    #     print(val["tradeDate"].tail(1))
    #     plt.title('{} plot'.format(key))
    #     val.closePrice.plot()
    #     # _tmp = copy.deepcopy(val.predictLabel)
    #     # _tmp = (_tmp + 1) /2 * val["closePrice"].min()
    #     # _tmp.plot()
    #     plt.show()


# if __name__ == "__main__":
stock_rdate_item = dict()
read_stock_base_read(stock_rdate_item)
print(stock_rdate_item.keys())
print(stock_rdate_item.values()[0].head(10))
