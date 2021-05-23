# -*- coding: utf-8 -*-
"""
Created on Tue May  4 18:52:31 2021



@author: TGalliz
"""

def cleanup_yahoodataframe(df):
    '''
    Cleans a yahoo finance dataframe and keeps only the Adj Close values
    Removes any columns with NaN
    

    Parameters
    ----------
    df : panda dataframe
        Raw dataframe from yahoo finance

    Returns
    -------
    df : panda dataframe
        Yahoo finance 

    '''
    import math
    
    if df.index.nlevels == 2:
        df  = df.droplevel(0,axis=1)
    
    df = df.drop(labels=['High','Low','Open','Close','Volume'],axis=1)
    
    df = df.dropna(axis=1, how = 'all')
    
    for x in df:
        if math.isnan(df[x][0]):
            df.pop(x)
            
    return df
 
def clean_dict(dico,threshold = 0.001):
    '''
    Clean efficient boundary to remove too small values
    Threshold = 0.001

    Parameters
    ----------
    dico : Efficient boundary output dictionary
        3 columns: TICKER, NAME, VALUE

    Returns
    -------
    dico : Efficient boundary output dictionary
        3 columns: TICKER, NAME, VALUE
    '''
    
    dico_t = dico.copy()
    
    for key, value in dico.items():
      if value < threshold:
        del dico_t[key]
        
    return dico_t 

def annual_return(stocks):
    '''
    Calculates the annual return on the stock 

    Parameters
    ----------
    stock : dataframe
    stock data with dates as index

    Returns
    -------
    dictionnary of annual return with symbol
    annual return %
    '''
    dicto = []
    for x in stocks:
        beg = stocks[x][0]
        
        

def get_company_name(symbol):
    import requests
    '''
    Get Company name from yahoo finance API 
    
    Parameters
    ----------
    symbol : string
        Financial ticker symbol

    Returns
    -------
    string
        Company name 

    '''
    
    url = 'http://d.yimg.com/autoc.finance.yahoo.com/autoc?query='+symbol+'&region=1&lang=en'
    result = requests.get(url).json()
    for r in result['ResultSet']['Result']:
      if r['symbol']==symbol:
        return r['name']