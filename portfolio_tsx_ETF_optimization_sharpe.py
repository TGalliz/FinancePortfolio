# -*- coding: utf-8 -*-
"""
Created on Sat May  1 11:49:39 2021

@author: Nietz
"""
import pandas as pd
import numpy as np
import requests
import pickle
import yfinance as yf

from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns

import SupportFuncFinance as sup

from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices

start_date = '2017-03-01'
end_date = '2021-04-14'

#Store data
df_tsx_etf = pd.read_csv('TSX_ETFs_clean_v2.csv')


#%%
data_tsx_etf_temp = y, f.download(df_tsx_etf['Toronto Ticker'].tolist(),start=start_date,end=end_date,actions = True)

#%%
data_tsx_etf_temp.to_pickle('data_tsx_etf.pkl')
#%%
data_tsx_etf = pickle.load(open('data_tsx_etf.pkl','rb'))

try:
    data_tsx_etf = sup.cleanup_yahoodataframe(data_tsx_etf)    
except:
    
    print('hello')

#%%
import math

for x in data_tsx_etf:
    
    if math.isnan(data_tsx_etf[x][-1]):
        print(x)
        data_tsx_etf_temp.pop(x)
  
#%%        
for x in range(0,data_tsx_etf.shape[1]-1):
    if math.isnan(data_tsx_etf.iloc[x,0]):
        data_tsx_etf.drop(data_tsx_etf.iloc[x])
    
    
#%%
i = 0
for x in df_tsx_etf['Toronto Ticker']:
    if x not in data_tsx_etf.columns:
        print(x)
        df_tsx_etf = df_tsx_etf[df_tsx_etf['Toronto Ticker'] != x]
#%%

df_tsx_etf.to_csv('TSX_ETFs_clean.csv')

#%%
mu_tsx_etf = expected_returns.mean_historical_return(data_tsx_etf)
                                                 
s_tsx_etf = risk_models.sample_cov(data_tsx_etf)


#%%
#Create the Efficient Frontier Object
ef_tsx_etf = EfficientFrontier(mu_tsx_etf, s_tsx_etf)
weights_tsx_etf = ef_tsx_etf.max_sharpe()
weights_tsx_etf = ef_tsx_etf.clean_weights()

weights_tsx_etf  = sup.clean_dict(weights_tsx_etf,0.01)
ef_tsx_etf.portfolio_performance(verbose=True)
#%%
weights_tsx_etf = sup.clean_dict(weights_tsx_etf,0.01)
#%%
# Get the discrete allocation of each share per stock

portfolio_val = 10000
latest_prices_tsx_etf = get_latest_prices(df_tsx_etf)

da_tsx_etf = DiscreteAllocation(weights_tsx_etf, latest_prices_tsx_etf, total_portfolio_value = portfolio_val)
allocation_tsx_etf, leftover_tsx_etf = da_tsx_etf.lp_portfolio()
print('Discrete Allocation:', allocation_tsx_etf)
print('Funds remaining: $', leftover_tsx_etf )
#%%

#Store the company name into a list
company_name_tsx_etf = []
for symbol in allocation_tsx_etf:
  company_name_tsx_etf.append(get_company_name(symbol[1]))

#Get the discrte allocation values
discrete_allocation_list_tsx_etf = []
for symbol in allocation_tsx_etf:
  discrete_allocation_list_tsx_etf.append(allocation_tsx_etf.get(symbol))

portfolio_df_tsx_etf = pd.DataFrame(columns = ['Company_name', 'Company_Ticker','Discrete_val_'+str(portfolio_val)])

portfolio_df_tsx_etf['Company_name'] = company_name_tsx_etf 
portfolio_df_tsx_etf['Company_Ticker'] = allocation_tsx_etf 
portfolio_df_tsx_etf['Discrete_val_'+str(portfolio_val)] = discrete_allocation_list_tsx_etf
portfolio_df_tsx_etf.sort_values(by='Discrete_val_'+str(portfolio_val),ascending=False)