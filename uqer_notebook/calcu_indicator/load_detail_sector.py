# -*- coding: utf-8 -*-

def dataframe_add_columns(t_df, columns, res_data):
    # columns = ["jump_up_date", "jump_dn_date"]
    # res_data = [0, 0]
    for _col, _res in zip(columns, res_data):
        t_df = pd.concat([t_df, pd.DataFrame(columns=list('A'))])
        t_df.rename(columns={'A': _col}, inplace=True)
        t_df[_col] = t_df[_col].apply(lambda x: _res)
    return t_df

def dataframe_select_drop_cols(t_df, columns, res_data):
    # columns = ["toST"]
    # res_data = [1]
    for _col, _res in zip(columns, res_data):
        t_df = t_df[t_df[_col] == _res]
        t_df = t_df.drop([_col], axis=1)
    return t_df

def delete_st_stock(stock_base):
	# delete ST stock
	stock_base = dataframe_add_columns(stock_base, ["toST"], [0])
	stock_base["toST"] = stock_base["secShortName"].apply(lambda x: 1 if "ST" in x or "st" in x else 0)
	stock_base = stock_base[stock_base["toST"] != 1]
	stock_base = stock_base.drop(["toST"], axis=1)
	# print stock_base.head()
	return stock_base


def load_stock_sector(stock_base):
	# secID have to be in stock_base !
	# 000001 上证综指 399106 深证综指 399001 深证成指
	# 399903 中证100 399905 中证500 000852 中证1000
	# 000300 沪深300 399005 中小100 399008 中小300
	# 000132 上证100 000010 上证180 000009 上证380
	# 399330 深证100 399009 深证200 399007 深证300
	stock_allinone = {
		"shzs": "000001", "szzz": "399106", "szcz": "399001",
		"zz100": "399903", "zz500": "399905", "zz1000": "000852",
		"hs300": "000300", "zx100": "399005", "zx300": "399008",
		"sh100": "000132", "sh180": "000010", "sh380": "000009",
		"sz100": "399330", "sz200": "399009", "sz300": "399007"
	}
	stock_allinone_rt = {k: [] for k, v in stock_allinone.items()}
	stock_allinone_rt_invert = dict()
	for key, val in stock_allinone.items():
		res = DataAPI.IdxConsGet(secID=u"", ticker=val, isNew=u"1", intoDate=u"", field=u"", pandas="1")
		stock_allinone_rt[key] = res.consID.to_dict().values()
	for key, vals in stock_allinone_rt.items():
		for val in vals:
			if val not in stock_allinone_rt_invert:
				stock_allinone_rt_invert[val] = []
			stock_allinone_rt_invert[val].append(key)

	_columns = stock_allinone.keys()
	_res_data = [0 for _ in range(len(_columns))]
	stock_base = dataframe_add_columns(stock_base, _columns, _res_data)
	for key, vals in stock_allinone_rt_invert.items():
		for val in vals:
			stock_base.loc[stock_base["secID"] == key, val] = 1
	stock_base = delete_st_stock(stock_base)
	return stock_base


def load_sw_industry(stock_base):
	# secID have to be in stock_base !
	stock_secIDs = stock_base.secID.to_dict().values()
	# print (stock_secIDs)
	_field = [
		"secID",  # str 通联编制的证券编码，可在DataAPI.SecIDGet获取到。
		# "ticker",  #  str 通用交易代码
		# "secShortName",  #    str 证券简称
		"industry",  # str 行业分类标准
		"industryID",  # str 行业分类编码，成分记录在最后一级行业分类下，上级行业请查看对应的一二三四级行业编码
		"industrySymbol",  # str 行业分类编码，行业编制机构发布的行业编码
		"isNew",  # int 是否最新：1-是，0-否
		"industryID1",  # str 一级行业编码
		"industryName1",  # str 一级行业
		"industryID2",  # str 二级行业编码
		"industryName2",  # str 二级行业
		"industryID3",  # str 三级行业编码
		"industryName3",  # str 三级行业
	]
	t_stock_base = DataAPI.EquIndustryGet(secID=stock_secIDs, ticker=u"", industryVersionCD=u"010303", industry=u"",
										  industryID=u"", industryID1=u"", industryID2=u"", industryID3=u"",
										  intoDate=u"", equTypeID=u"", field=_field, pandas="1")
	t_stock_base = dataframe_select_drop_cols(t_stock_base, ["isNew"], [1])
	# print stock_base.head()
	# print len(stock_base)
	stock_base = pd.merge(stock_base, t_stock_base, how='left', on='secID')
	stock_base.drop_duplicates(subset="secID", keep="first", inplace=True)
	stock_base.dropna(subset=["secID", "industry", "industryID", "industrySymbol"], axis=0, inplace=True)
	# print (stock_base.head())
	# print (len(stock_base))
	return stock_base


# if __name__ == "__main__":
stock_newest_random = stock_newest_random.sample(n=50)  # 随机选择50支股票
stock_newest_random = load_stock_sector(stock_newest_random)
stock_newest_random = load_sw_industry(stock_newest_random)

_pd_sw_id1 = pd.get_dummies(stock_newest_random["industryName1"], prefix="sw_id1")
_pd_sw_id2 = pd.get_dummies(stock_newest_random["industryName2"], prefix="sw_id2")
_pd_sw_id3 = pd.get_dummies(stock_newest_random["industryName3"], prefix="sw_id3")
stock_newest_random = pd.concat([stock_newest_random, _pd_sw_id1], axis=1)
stock_newest_random = pd.concat([stock_newest_random, _pd_sw_id2], axis=1)
stock_newest_random = pd.concat([stock_newest_random, _pd_sw_id3], axis=1)

stock_newest_random.head(5)