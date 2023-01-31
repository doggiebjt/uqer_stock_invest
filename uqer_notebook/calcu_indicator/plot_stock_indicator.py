import matplotlib.pyplot as plt

_field = [
    u'secID', u'ticker', u'secShortName', u'tradeDate',
    u'openPrice', u'highestPrice', u'lowestPrice', u'closePrice',
    u'negMarketValue', u'marketValue', u'turnoverRate', u'turnoverValue', u'dealAmount',
    u'accumAdjFactor', u'PE', u'PB', u'ROE', u'isOpen', u'vwap'
]

stock_rdate = [  \
 ('600835', '2014-07-01', '2022-12-16'),
 ('000921', '2014-07-01', '2022-12-16'),
 ('000528', '2014-07-01', '2020-12-16'),
 ('002543', '2014-07-01', '2020-12-16'),
 ('600993', '2014-07-01', '2022-12-16'),
]

for _ticker, start_day, end_day in stock_rdate:
    # 沪深股票前复权行情
    res = DataAPI.MktEqudAdjGet(secID=u"", ticker=_ticker, tradeDate="", beginDate=start_day, endDate=end_day, isOpen="", field=_field, pandas="1")
    res = res[res["isOpen"] == 1]
    res.drop(["secID", "isOpen", "vwap", "accumAdjFactor"], axis=1, inplace="True")

    plt.title('{} plot'.format(_ticker))
    res.closePrice.plot()
    plt.show()
    # res.dealAmount.plot()
    # plt.show()
    # _t = res.negMarketValue / res.dealAmount
    # _t.rolling(10).mean().plot()
    # plt.show()
    # res.negMarketValue.plot()
    # plt.show()
    # _t = res.negMarketValue / res.closePrice
    # _t.plot()
    # plt.show()
