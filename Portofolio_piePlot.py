# -*- coding: utf-8 -*-
"""
Created on Fri Mar 12 07:32:04 2021

@author: Nietz
"""



#Imports
import pandas as pd
import numpy as np
import requests

import yfinance as yf

# from pypfopt.efficient_frontier import EfficientFrontier
# from pypfopt import risk_models
# from pypfopt import expected_returns

# from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices

tsx_tickers = pd.read_csv('TSX_tickers.csv')
stocks = pd.read_csv('MULTI_20210326.csv')

sectors = []
industries = []
for ticker in stocks['Symbole']:
    print(ticker)
    data = yf.Ticker(ticker)
    try:
        print('Sector: ' + data.get_info()['sector']+ ' Industry: ' + data.get_info()['industry'])
        sectors.append(data.get_info()['sector'])
        industries.append(data.get_info()['industry'])
    except:
        try:
            ticker = ticker.replace('.','-',1)
            print(ticker)
            data = yf.Ticker(ticker)
            print('Sector: ' + data.get_info()['sector']+ ' Industry: ' + data.get_info()['industry'])
            sectors.append(data.get_info()['sector'])
            industries.append(data.get_info()['industry'])
        except:
            print('Problem getting data for:' + ticker)
            sectors.append('NONE')
            industries.append('NONE')


stocks['sectors'] = sectors
stocks['industries'] = industries

#%%
import seaborn as sbs
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
import numpy as np

#%%
def find_sector(data,specific_indus):
    i = -1
    for industries in data:
        i +=1
        for indus in industries:
                if indus == specific_indus:
                    return data.index[i]

def create_inner_colors(df,outer_colors):
    sectors = df.groupby('sectors', sort=False)['Valeur marchande'].sum()
    keys = sectors.keys()
    dictt = stocks.groupby('sectors',sort=False)['industries'].unique()
    industries = df.groupby('industries', sort=False)['Valeur marchande'].sum()
    
    lis = outer_colors.tolist()
    outer_col_ser = pd.Series(lis,index=keys)

    
    inner_colors = []
    industr = industries.index
    for indus in industr:
        sector = find_sector(dictt,indus)
        inner_colors.append(outer_col_ser[sector])
        print(sector +  '  ' + indus)\
    
    inner_colors = np.array(inner_colors)
    return inner_colors

df = stocks.copy()
df = df.sort_values(by=['sectors'])

import matplotlib.pyplot as plt
cmap = plt.get_cmap("tab10")

outer_colors = cmap(np.arange(len(df.groupby('sectors'))))   

inner_colors = create_inner_colors(df,outer_colors)


#%%       
 
fig, ax = plt.subplots(figsize=(12.2,6.4))

size = 0.3

wedges, text = ax.pie(df.groupby('sectors', sort=False)['Valeur marchande'].sum(),center=(0,0), explode=[0.05]*len(df.groupby('sectors')), radius=1, pctdistance=0.85 ,startangle = -30, colors=outer_colors, wedgeprops=dict(width=size, edgecolor='w'))
# ax.legend(df['sectors'].drop_duplicates(),loc=6)

bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
kw = dict(arrowprops=dict(arrowstyle="-"),
          bbox=bbox_props, zorder=0, va="center")

for i, p in enumerate(wedges):
    ang = (p.theta2 - p.theta1)/2. + p.theta1
    y = np.sin(np.deg2rad(ang))
    x = np.cos(np.deg2rad(ang))
    horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
    connectionstyle = "angle,angleA=0,angleB={}".format(ang)
    kw["arrowprops"].update({"connectionstyle": connectionstyle})
    ax.annotate(df['sectors'].drop_duplicates().to_list()[i], xy=(x, y), xytext=(1.35*np.sign(x), 1.4*y),
                horizontalalignment=horizontalalignment, **kw)


ax.pie(df.groupby('industries', sort=False)['Valeur marchande'].sum(),center=(0,0), radius=1-size, explode=[0.00]*len(df.groupby('industries')), colors=inner_colors,startangle = -30,wedgeprops=dict(width=size, edgecolor='w'))

ax.set(aspect="equal", title='Sectors')
plt.show()

# #%%
# '''
# Get Sharpe ratio for all stocks
# '''
# from pypfopt.efficient_frontier import EfficientFrontier
# from pypfopt import risk_models
# from pypfopt import expected_returns
# from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices

# data_tsx = yf.download(df['Symbole'].tolist(),start='2015-01-01',end='2021-01-31')