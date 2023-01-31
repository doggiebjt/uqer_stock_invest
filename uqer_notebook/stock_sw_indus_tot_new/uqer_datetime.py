# -*- coding: utf-8 -*-
# utils by wukesonguo
from CAL.PyCAL import *

import numpy as np
import pandas as pd

import json
import copy
import datetime

from matplotlib import pyplot as plt

pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_columns', 1000)
pd.set_option('display.width', 1000)

cal = Calendar('China.SSE')

_current_date = datetime.date.today()
# current_date = cal.adjustDate(_current_date, BizDayConvention.Preceding)
current_date = _current_date

span_prev_date = Period('-1B')  # last day
span_one_year_date = Period('-12M')
span_two_year_date = Period('-24M')
span_ten_year_date = Period('-60M')  # 10 years
# span_ten_year_date = Period('-180M')  # 15 years

_last_date = cal.advanceDate(current_date, span_prev_date)  # "2022-12-01"
last_date = cal.adjustDate(_last_date, BizDayConvention.Preceding)

_one_year_date = cal.advanceDate(last_date, span_one_year_date)  # "2021-12-02"
_two_year_date = cal.advanceDate(last_date, span_two_year_date)  # "2020-12-02"
_ten_year_date = cal.advanceDate(last_date, span_ten_year_date)  # "2020-12-02"

one_year_date = cal.adjustDate(_one_year_date, BizDayConvention.Preceding)  # 前一年剔除非交易日
two_year_date = cal.adjustDate(_two_year_date, BizDayConvention.Preceding)  # 前两年剔除非交易日
ten_year_date = cal.adjustDate(_ten_year_date, BizDayConvention.Preceding)  # 前十年剔除非交易日

stock_periodic = []
_s_dates = [6 * (_ + 1) for _ in range(30)]  # 30 * 6 months
_e_dates = [6 * _ for _ in range(30)]
for _s_date, _e_date in zip(_s_dates, _e_dates):
	span_s_date = Period('-{}M'.format(_s_date))
	span_e_date = Period('-{}M'.format(_e_date))
	t_s_date = cal.advanceDate(last_date, span_s_date)
	t_e_date = cal.advanceDate(last_date, span_e_date)
	t_s_date = cal.adjustDate(t_s_date, BizDayConvention.Preceding)
	t_e_date = cal.adjustDate(t_e_date, BizDayConvention.Preceding)
	stock_periodic.append((t_s_date, t_e_date))

s_date = ten_year_date
e_date = current_date
def extract_trade_dates(s_date, e_date):
	# trade dates from s_date to e_date -> [s_date, e_date]
	_field = [
		u'calendarDate', u'prevTradeDate', u'isWeekEnd', u'isMonthEnd', u'isQuarterEnd', u'isYearEnd'
	]
	XSHG_DATES = DataAPI.TradeCalGet(exchangeCD=u"XSHG", beginDate=s_date, endDate=e_date, isOpen=u"1", field=_field, pandas="1")  # 前闭后闭
	XSHE_DATES = DataAPI.TradeCalGet(exchangeCD=u"XSHE", beginDate=s_date, endDate=e_date, isOpen=u"1", field=_field, pandas="1")  # 前闭后闭
	return XSHG_DATES, XSHE_DATES

XSHG_DATES, XSHE_DATES = extract_trade_dates(s_date, e_date)
print(XSHG_DATES.head(5))
print(XSHG_DATES.tail(5))
N_XSHG_DATES = [int(_.replace("-", "")) for _ in XSHG_DATES.calendarDate]
print(N_XSHG_DATES)

# 日期格式转换
# current_date = cal.adjustDate(_current_date, BizDayConvention.Preceding)
s_current_date = str(current_date)
n_current_date = int(s_current_date.replace("-", ""))
s_last_date = str(last_date)
n_last_date = int(s_last_date.replace("-", ""))

s_one_year_date = str(one_year_date)
n_one_year_date = int(s_one_year_date.replace("-", ""))
s_two_year_date = str(two_year_date)
n_two_year_date = int(s_two_year_date.replace("-", ""))
s_ten_year_date = str(ten_year_date)
n_ten_year_date = int(s_ten_year_date.replace("-", ""))
print(s_current_date, s_last_date, s_one_year_date, s_two_year_date, s_ten_year_date)
print(n_current_date, n_last_date, n_one_year_date, n_two_year_date, n_ten_year_date)
