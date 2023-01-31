# -*- coding: utf-8 -*-
import pandas as pd
import copy
import math


def find_jump_dn_stock(jump_up_allinone, price_df, min_jump_thres=0.01, max_jump_thres=0.04, buy_in_rate=0.95,
					   sell_out_rate=0.90, max_res_days=20):
	ticker = price_df['ticker'][0]
	secShortName = price_df['secShortName'][0]

	jump_up_items = []
	for idx in price_df.index:
		if idx <= 4: continue
		# p_tradeDate = price_df['tradeDate'][idx-1]
		# p_openPrice = price_df['openPrice'][idx-1]
		p_closePrice = price_df['closePrice'][idx - 1]
		p_highestPrice = price_df['highestPrice'][idx - 1]
		p_lowestPrice = price_df['lowestPrice'][idx - 1]
		# p_turnoverRate = price_df['turnoverRate'][idx-1]

		p_turnoverRate_5days_avg = sum(price_df['turnoverRate'][idx - 5: idx]) / 5  # 过去五天的成交量均值

		tradeDate = price_df['tradeDate'][idx]
		# openPrice = price_df['openPrice'][idx]
		closePrice = price_df['closePrice'][idx]
		highestPrice = price_df['highestPrice'][idx]
		lowestPrice = price_df['lowestPrice'][idx]
		turnoverRate = price_df['turnoverRate'][idx]

		jump_up_rate = (highestPrice - p_lowestPrice) / p_lowestPrice
		jump_up_rate = -jump_up_rate
		# jump down condition
		if jump_up_rate >= min_jump_thres and jump_up_rate <= max_jump_thres:
			if idx + max_res_days >= len(price_df['tradeDate']): continue  # max_res_days
			jump_up_items.append(
				[idx, idx + max_res_days, tradeDate, ticker, secShortName, lowestPrice, closePrice, highestPrice,
				 p_highestPrice, p_closePrice, p_lowestPrice, turnoverRate / p_turnoverRate_5days_avg])

	for _packs in jump_up_items:
		[s_idx, e_idx, tradeDate, _, _, lowestPrice, closePrice, highestPrice,
		 p_highestPrice, p_closePrice, p_lowestPrice, _] = _packs

		p_lowestPrice_5pt = p_lowestPrice * buy_in_rate  # buy in
		p_lowestPrice_10pt = p_lowestPrice * sell_out_rate  # sell out
		p_lowestPrice_5pt_days = -1
		p_lowestPrice_10pt_days = -1
		jump_back_day_5pt = -1
		jump_back_day_10pt = -1

		highestPrice_s = list(price_df['highestPrice'][s_idx: e_idx])
		lowestPrice_s = list(price_df['lowestPrice'][s_idx: e_idx])
		openPrice_s = list(price_df['openPrice'][s_idx: e_idx])
		closePrice_s = list(price_df['closePrice'][s_idx: e_idx])

		for idx_, (highestPrice_, lowestPrice_, openPrice_, closePrice_) in enumerate(
				zip(highestPrice_s, lowestPrice_s, openPrice_s, closePrice_s)):
			# TODO: make sure that can buy in stock
			if lowestPrice_ <= p_lowestPrice_5pt and p_lowestPrice_5pt_days == -1:
				p_lowestPrice_5pt_days = idx_
			if lowestPrice_ <= p_lowestPrice_10pt and highestPrice_ >= lowestPrice_ * 1.010 and p_lowestPrice_5pt_days != -1 and p_lowestPrice_10pt_days == -1:
				p_lowestPrice_10pt_days = idx_
			if highestPrice_ >= p_lowestPrice * 1.005 and p_lowestPrice_5pt_days != -1 and jump_back_day_5pt == -1:
				jump_back_day_5pt = idx_
			if highestPrice_ >= p_lowestPrice * 1.005 and p_lowestPrice_10pt_days != -1 and jump_back_day_10pt == -1:
				jump_back_day_10pt = idx_

		closePrice_30days = (closePrice_s[-1] / p_lowestPrice) - 1

		_packs.extend([p_lowestPrice_5pt_days, jump_back_day_5pt, p_lowestPrice_10pt_days, jump_back_day_10pt,
					   closePrice_30days])
	# print jump_up_items
	jump_up_allinone[secShortName] = copy.deepcopy(jump_up_items)


def stock_dn_stastics(jump_dn_allinone, secIDS, start_day, end_day, _min_jump_thres=0.01, _max_jump_thres=0.04,
					  _buy_in_rate=0.950, _sell_out_rate=0.900, _max_res_days=20):
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
		stock_result = DataAPI.MktEqudAdjGet(secID=secID, ticker=u"", tradeDate=u"", beginDate=start_day,
											 endDate=end_day, isOpen="1", field=_field, pandas="1")
		find_jump_dn_stock(jump_dn_allinone, stock_result,
						   min_jump_thres=_min_jump_thres, max_jump_thres=_max_jump_thres,
						   buy_in_rate=_buy_in_rate, sell_out_rate=_sell_out_rate, max_res_days=_max_res_days)
	# print(jump_up_allinone)

	_jump_dn_stock = [
		u's_idx', u'e_idx', u'tradeDate', u'ticker', u'secShortName',
		u'lowestPrice', u'closePrice', u'highestPrice',
		u'p_highestPrice', u'p_closePrice', u'p_lowestPrice', u'turnoverIncreaseRate',
		u'p_lowestPrice_5pt_days', u'jump_back_day_5pt',
		u'p_lowestPrice_10pt_days', u'jump_back_day_10pt', u'closePrice_30days']
	_jump_dn_allinone = []
	for key, val in jump_dn_allinone.items():
		_jump_dn_allinone.extend(val)
	_jump_dn_allinone = pd.DataFrame(_jump_dn_allinone, columns=_jump_dn_stock)

	s_5_jump_dn_allinone = copy.deepcopy(_jump_dn_allinone)
	# print(len(s_5_jump_dn_allinone))
	# s_5_jump_up_allinone.drop("secShortName", inplace=True, axis=1)
	s_5_jump_dn_allinone = s_5_jump_dn_allinone[s_5_jump_dn_allinone['tradeDate'] != -1]
	print(len(s_5_jump_dn_allinone))
	# term 1 成交量未出现明显放大
	s_5_jump_dn_allinone = \
		s_5_jump_dn_allinone[s_5_jump_dn_allinone['turnoverIncreaseRate'] <= 2.0]
	print(len(s_5_jump_dn_allinone))
	# term 2 跳空当天收盘价未出现跌停（盘中未出现跌停）
	s_5_jump_dn_allinone = \
		s_5_jump_dn_allinone[s_5_jump_dn_allinone['closePrice'] >= s_5_jump_dn_allinone['p_closePrice'] * 0.91]
	print(len(s_5_jump_dn_allinone))

	# term 3 stastics result
	s_5_jump_dn_allinone = s_5_jump_dn_allinone[s_5_jump_dn_allinone['p_lowestPrice_5pt_days'] != -1]
	print(len(s_5_jump_dn_allinone))
	jump_down_spilt_days = 2
	print("s_5_jump_dn_allinone['p_lowestPrice_5pt_days'] < {}".format(jump_down_spilt_days))
	s_5_jump_dn_allinone = s_5_jump_dn_allinone[s_5_jump_dn_allinone['p_lowestPrice_5pt_days'] < jump_down_spilt_days]
	s_5_jump_dn_5pt_cnt = len(s_5_jump_dn_allinone)
	print(s_5_jump_dn_5pt_cnt)
	# s_5_jump_dn_allinone_x = s_5_jump_dn_allinone[s_5_jump_dn_allinone['p_lowestPrice_10pt_days'] == -1]
	s_5_jump_dn_allinone = s_5_jump_dn_allinone[s_5_jump_dn_allinone['p_lowestPrice_10pt_days'] >= jump_down_spilt_days]
	s_5_jump_dn_10pt_cnt = len(s_5_jump_dn_allinone)
	print(s_5_jump_dn_10pt_cnt)
	# stastics result
	print("stastics result")
	print(len(s_5_jump_dn_allinone[s_5_jump_dn_allinone['p_lowestPrice_5pt_days'] >= 1]))
	print(len(s_5_jump_dn_allinone[s_5_jump_dn_allinone['jump_back_day_5pt'] >= 1]))
	print(len(s_5_jump_dn_allinone[s_5_jump_dn_allinone['p_lowestPrice_10pt_days'] >= 1]))
	print(len(s_5_jump_dn_allinone[s_5_jump_dn_allinone['jump_back_day_10pt'] >= 1]))


if __name__ == '__main__':
	# # for test
	# from data_simulation import s_jump_up_allinone
	# jump_up_allinone = s_jump_up_allinone

	start_day = four_year_day
	end_day = last_day

	# 000300 沪深300 000001 上证综指 399106 深证综指 399001 深证成指
	_field = [u'intoDate', u'consID', u'consShortName',
			  u'consTickerSymbol', u'consExchangeCD', u'isNew']
	secIDS = []
	# secIDS = ["000333.XSHE", "000651.XSHE"]  # for test
	for _ticker in [u"000300"]:
		res = DataAPI.IdxConsGet(secID=u"", ticker=_ticker, isNew=u"1", intoDate=u"", field=_field, pandas="1")
		secIDS = secIDS + res.consID.to_dict().values()
	secIDS = list(set(secIDS))

	# simulation parameters
	s_min_jump_thres = [
		0.010, 0.010, 0.010,  # 1
		0.010, 0.010, 0.010,  # 2
		0.010, 0.010, 0.010,  # 3
		0.010, 0.010, 0.010,  # 4
	]
	s_max_jump_thres = [
		0.040, 0.040, 0.040,  # 1
		0.040, 0.040, 0.040,  # 2
		0.040, 0.040, 0.040,  # 3
		0.040, 0.040, 0.040,  # 4
	]
	s_buy_in_rate = [
		0.950, 0.950, 0.950,  # 1
		0.955, 0.955, 0.955,  # 2
		0.960, 0.960, 0.960,  # 3
		0.965, 0.965, 0.965,  # 4
	]
	s_sell_out_rate = [
		0.900, 0.900, 0.900,  # 1
		0.895, 0.895, 0.895,  # 2
		0.890, 0.890, 0.890,  # 3
		0.885, 0.885, 0.885,  # 4
	]
	s_max_res_days = [
		15, 30, 60,  # 1
		15, 30, 60,  # 2
		15, 30, 60,  # 3
		15, 30, 60,  # 4
	]

	for _min_jump_thres, _max_jump_thres, _buy_in_rate, _sell_out_rate, _max_res_days in \
			zip(s_min_jump_thres, s_max_jump_thres, s_buy_in_rate, s_sell_out_rate, s_max_res_days):
		jump_dn_allinone = {}
		print(_min_jump_thres, _max_jump_thres, _buy_in_rate, _sell_out_rate, _max_res_days)
		stock_dn_stastics(jump_dn_allinone, secIDS, start_day, end_day, _min_jump_thres, _max_jump_thres, _buy_in_rate,
						  _sell_out_rate, _max_res_days)
		print(jump_dn_allinone)
