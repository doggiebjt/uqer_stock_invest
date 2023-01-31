# -*- coding: utf-8 -*-
import pandas as pd
import copy


def find_jump_up_stock(jump_up_allinone, price_df, min_jump_thres=0.01, max_jump_thres=0.04, buy_in_rate=1.04, sell_out_rate=1.16, max_res_days=20):
    ticker = price_df['ticker'][0]
    secShortName = price_df['secShortName'][0]
    
    jump_up_items = []
    for idx in price_df.index:
        if idx <= 4: continue
        # p_tradeDate = price_df['tradeDate'][idx-1]
        # p_openPrice = price_df['openPrice'][idx-1]
        p_closePrice = price_df['closePrice'][idx-1]
        p_highestPrice = price_df['highestPrice'][idx-1]
        # p_lowestPrice = price_df['lowestPrice'][idx-1]
        # p_turnoverRate = price_df['turnoverRate'][idx-1]   

        p_turnoverRate_5days_avg = sum(price_df['turnoverRate'][idx-5: idx]) / 5  # 过去五天的成交量均值
    
        tradeDate = price_df['tradeDate'][idx]
        # openPrice = price_df['openPrice'][idx]
        closePrice = price_df['closePrice'][idx]
        highestPrice = price_df['highestPrice'][idx]
        lowestPrice = price_df['lowestPrice'][idx]
        turnoverRate = price_df['turnoverRate'][idx]  

        jump_up_rate = (lowestPrice - p_highestPrice) / p_highestPrice
        # jump_up_rate = -jump_up_rate
        if jump_up_rate >= min_jump_thres and jump_up_rate <= max_jump_thres: 
            if idx + max_res_days >= len(price_df['tradeDate']): continue  # max_res_days 
            jump_up_items.append([idx, idx + max_res_days, tradeDate, ticker, secShortName, lowestPrice, closePrice, highestPrice, p_highestPrice, p_closePrice, turnoverRate / p_turnoverRate_5days_avg])

    for _packs in jump_up_items:
        [s_idx, e_idx, tradeDate, _, _, lowestPrice, closePrice, highestPrice, p_highestPrice, p_closePrice, _] = _packs

        p_highestPrice_5pt = p_highestPrice * buy_in_rate  # buy in
        p_highestPrice_10pt = p_highestPrice * sell_out_rate  # sell out
        p_highestPrice_5pt_days = -1
        p_highestPrice_10pt_days = -1
        jump_back_day_5pt = -1
        jump_back_day_10pt = -1

        highestPrice_s = list(price_df['highestPrice'][s_idx: e_idx])
        lowestPrice_s = list(price_df['lowestPrice'][s_idx: e_idx])
        openPrice_s = list(price_df['openPrice'][s_idx: e_idx])
        closePrice_s = list(price_df['closePrice'][s_idx: e_idx])

        for idx_, (highestPrice_, lowestPrice_, openPrice_, closePrice_) in enumerate(zip(highestPrice_s, lowestPrice_s, openPrice_s, closePrice_s)):
            # make sure that can buy in 5pt
            if highestPrice_ >= p_highestPrice_5pt and lowestPrice_ <= p_highestPrice_5pt * 0.995 and p_highestPrice_5pt_days == -1:
                p_highestPrice_5pt_days = idx_

            if highestPrice_ >= p_highestPrice_10pt and p_highestPrice_5pt_days != -1 and p_highestPrice_10pt_days == -1:
                p_highestPrice_10pt_days = idx_

            if lowestPrice_ <= p_highestPrice * 0.995 and p_highestPrice_5pt_days != -1 and jump_back_day_5pt == -1:
                jump_back_day_5pt = idx_

            if lowestPrice_ <= p_highestPrice * 0.995 and p_highestPrice_10pt_days != -1 and jump_back_day_10pt == -1:
                jump_back_day_10pt = idx_

        closePrice_30days = (closePrice_s[-1] / p_highestPrice) - 1
        
        _packs.extend([p_highestPrice_5pt_days, jump_back_day_5pt, p_highestPrice_10pt_days, jump_back_day_10pt, closePrice_30days])
    # print jump_up_items
    jump_up_allinone[secShortName] = copy.deepcopy(jump_up_items)


if __name__ == '__main__':
    # from data_simulation import s_jump_up_allinone
    # jump_up_allinone = s_jump_up_allinone

    start_day = four_year_day
    end_day = last_day

    # 000300 沪深300 000001 上证综指 399106 深证综指 399001 深证成指
    res = DataAPI.IdxConsGet(secID=u"", ticker=u"000300", isNew=u"1", intoDate=u"", field=u"", pandas="1")
    secIDS = res.consID.to_dict().values()
    
    jump_up_allinone = {}
    jump_dn_allinone = {}
    # secIDS = ["000333.XSHE", "000651.XSHE"]  # for test
    for secID in secIDS:
        start_day = str(start_day).replace("-", "")
        end_day = str(end_day).replace("-", "")
        _field = [
            u'secID', u'ticker', u'secShortName', u'exchangeCD', u'tradeDate',
            u'preClosePrice', u'actPreClosePrice', u'openPrice', u'highestPrice',
            u'lowestPrice', u'closePrice', u'turnoverVol', u'negMarketValue',
            u'dealAmount', u'turnoverRate', u'accumAdjFactor', u'turnoverValue',
            u'marketValue', u'chgPct', u'PE', u'PB', u'isOpen', u'vwap'
        ]
        # 沪深股票前复权行情
        stock_result = DataAPI.MktEqudAdjGet(secID=secID, ticker=u"", tradeDate=u"", beginDate=start_day, endDate=end_day,
                                    isOpen="1", field=_field, pandas="1")
        # print stock_result.head(10)
        find_jump_up_stock(jump_up_allinone, stock_result)
    print(jump_up_allinone)

    _jump_up_stock = [
        u's_idx', u'e_idx', u'tradeDate', u'ticker', u'secShortName',
        u'lowestPrice', u'closePrice', u'highestPrice', 
        u'p_highestPrice', u'p_closePrice', u'turnoverIncreaseRate',
        u'p_highestPrice_5pt_days', u'jump_back_day_5pt', 
        u'p_highestPrice_10pt_days', u'jump_back_day_10pt', u'closePrice_30days']
    _jump_up_allinone = []
    for key, val in jump_up_allinone.items():
        _jump_up_allinone.extend(val)
    _jump_up_allinone = pd.DataFrame(_jump_up_allinone, columns=_jump_up_stock) 
    # print(_jump_up_allinone.head(10))

    # output_up_stastic
    s_5_jump_up_allinone = copy.deepcopy(_jump_up_allinone)
    print(len(s_5_jump_up_allinone))
    # s_5_jump_up_allinone.drop("secShortName", inplace=True, axis=1)
    s_5_jump_up_allinone = s_5_jump_up_allinone[s_5_jump_up_allinone['tradeDate'] != -1]
    print(len(s_5_jump_up_allinone))
    # term 1 成交量未出现明显放大
    s_5_jump_up_allinone = \
    s_5_jump_up_allinone[s_5_jump_up_allinone['turnoverIncreaseRate'] <= 2.0]
    print(len(s_5_jump_up_allinone))
    # term 2 跳空当天收盘价未出现涨停（盘中未出现涨停）
    s_5_jump_up_allinone = \
    s_5_jump_up_allinone[s_5_jump_up_allinone['closePrice']  <= s_5_jump_up_allinone['p_closePrice'] * 1.09]
    # s_5_jump_up_allinone = s_5_jump_up_allinone[s_5_jump_up_allinone['highestPrice']  <= s_5_jump_up_allinone['p_closePrice'] * 1.09]
    print(len(s_5_jump_up_allinone))
    # term 3 关于买入点的约束条件
    s_5_jump_up_allinone = s_5_jump_up_allinone[s_5_jump_up_allinone['p_highestPrice_5pt_days'] != -1]
    s_5_jump_up_allinone = s_5_jump_up_allinone[s_5_jump_up_allinone['p_highestPrice_5pt_days'] <= 1]
    print(len(s_5_jump_up_allinone))
    s_5_jump_up_allinone_x = s_5_jump_up_allinone[s_5_jump_up_allinone['p_highestPrice_10pt_days'] == -1]
    s_5_jump_up_allinone = s_5_jump_up_allinone[s_5_jump_up_allinone['p_highestPrice_10pt_days'] >= 1]
    print(len(s_5_jump_up_allinone))
    # stastics result
    print("stastics result")
    print(len(s_5_jump_up_allinone[s_5_jump_up_allinone['p_highestPrice_5pt_days'] >= 0]))
    print(len(s_5_jump_up_allinone[s_5_jump_up_allinone['jump_back_day_5pt'] >= 1]))
    print(len(s_5_jump_up_allinone[s_5_jump_up_allinone['p_highestPrice_10pt_days'] >= 1]))
    print(len(s_5_jump_up_allinone[s_5_jump_up_allinone['jump_back_day_10pt'] >= 1]))
    # s_5_jump_up_allinone.to_csv("s_5_jump_up_stastics.csv")
    # print s_5_jump_up_allinone['p_highestPrice_10pt_days'].value_counts(ascending=False)

    # # 校对是否有集中分布的情况
    # temp = copy.deepcopy(s_5_jump_up_allinone['tradeDate'].apply(lambda x: x[:7]))
    # print temp.value_counts(ascending=False)

    # max_res_days
    print(s_5_jump_up_allinone_x['closePrice_30days'].mean())  # 未涨到10pt清仓条件
