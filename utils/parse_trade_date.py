# -*- coding: utf-8 -*-
from CAL.PyCAL import *
import datetime

cal = Calendar('China.SSE')
_current_date = datetime.date.today()
current_date = cal.adjustDate(_current_date, BizDayConvention.Preceding)

span_prev_date = Period('-1B')  # last day
span_one_year_date = Period('-12M')
span_two_year_date = Period('-24M')
span_ten_year_date = Period('-180M')  # 15 years

_last_date = cal.advanceDate(current_date, span_prev_date)  # "2022-12-01"
last_date = cal.adjustDate(_last_date, BizDayConvention.Preceding)

_one_year_date = cal.advanceDate(last_date, span_one_year_date)  # "2021-12-02"
_two_year_date = cal.advanceDate(last_date, span_two_year_date)  # "2020-12-02"
_ten_year_date = cal.advanceDate(last_date, span_ten_year_date)  # "2020-12-02"

one_year_date = cal.adjustDate(_one_year_date, BizDayConvention.Preceding)  # 前一年剔除非交易日
two_year_date = cal.adjustDate(_two_year_date, BizDayConvention.Preceding)  # 前两年剔除非交易日
ten_year_date = cal.adjustDate(_two_year_date, BizDayConvention.Preceding)  # 前十年剔除非交易日

print(current_date, last_date, one_year_date, two_year_date, ten_year_date)

s_date = two_year_date
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
print(XSHG_DATES)
