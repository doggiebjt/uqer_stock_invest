# -*- coding: utf-8 -*-
# utils by wukesonguo
import pandas as pd

import os
import json
import copy
import datetime

base_dir = "D:\workstation_spring_at_home\stock_research"
stock_tech_csv_walk = list(os.walk("{}\data\csv\stock_tech_indicator".format(base_dir)))
base_direction = stock_tech_csv_walk[0][0]
file_names = stock_tech_csv_walk[0][-1]

file_names = [base_direction + "\\" + _ for _ in file_names]
# print(file_names)

stock_tech_csvs = []
for file_name in file_names:
    stock_tech_csv = pd.read_csv(file_name)
    stock_tech_csvs.append(stock_tech_csv)

stock_tech_csv = pd.concat(stock_tech_csvs)
stock_tech_csv.dropna(subset=["tradeDate"], inplace=True)
stock_tech_csv.drop_duplicates(subset=["secID", "tradeDate"], keep="first", inplace=True)
stock_tech_csv.drop(["Unnamed: 0"], axis=1, inplace=True)
stock_tech_csv.sort_values(by=["secID", "tradeDate"], ascending=True, inplace=True)
stock_tech_csv.rename(columns={'tradeDate': "s_tradeDate"}, inplace=True)
stock_tech_secIDS = stock_tech_csv.secID.unique()
# import pdb; pdb.set_trace()
stock_tech_csv.to_csv('{}\data\csv\stock_tech_indicator_collect.csv'.format(base_dir), encoding='utf_8_sig')

stock_tech_items_dict = dict()
for secID in stock_tech_secIDS:
    stock_tech_item = stock_tech_csv[stock_tech_csv["secID"] == secID]
    stock_tech_items_dict[secID] = copy.deepcopy(stock_tech_item)

stock_newest_features = pd.read_csv("{}\data\csv\{}".format(base_dir, "stock_load_newest_indicator.csv"))
stock_newest_features.drop_duplicates(subset=["secID", "s_listDate"], keep="first", inplace=True)

print("Stock_tech_items load done.")
