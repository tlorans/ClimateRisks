# -*- coding: utf-8 -*-
"""
Created on Mon Jan  2 11:22:47 2023

@author: tlorans
"""

import requests
import time
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
import os
from selenium import webdriver
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.interaction import KEY
from selenium.webdriver.common import keys
import json
from webdriver_manager.chrome import ChromeDriverManager
import re 
from pandera.typing import DataFrame, DateTime, Object, Series
import pandera as pa
import yfinance as yf
from tqdm import tqdm
import urllib
import numpy as np

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
service = Service(executable_path=ChromeDriverManager().install())



def reformat(text:str) -> str:
    text=text.lower() 
    text=re.sub("\\W"," ",text) # remove special chars
    words=re.split("\\s+",text)
    # stem words
    words = [word for word in words if word != ""]
    return "-".join(words)

def get_yahoo_longname(symbol):
    response = urllib.request.urlopen(f'https://query2.finance.yahoo.com/v1/finance/search?q={symbol}')
    content = response.read()
    print(symbol)
    try:
        data = json.loads(content.decode('utf8'))['quotes'][0]['longname']
    except:
        data = ''
    return data

def generate_df(Stock_Tickers, list_quarters):

    
    df = pd.DataFrame()
    list_tickers = Stock_Tickers['Symbol']
    for ticker in list_tickers:
        stockname = get_yahoo_longname(ticker)
        stockname_formated = str(reformat(stockname))
        ticker_formated = str(reformat(ticker))
        df = pd.concat([df, pd.DataFrame({'Ticker':ticker, 
                                          'quarter':list_quarters,
                                          'StockName': stockname,
                                          'StockNameFormated':stockname_formated,
                                          'TickerFormated':ticker_formated
                                          
                                          })])
    
    return df
    
    
def process_page(row:Object):    
    driver = webdriver.Chrome(service=service,chrome_options=chrome_options)
    comp_name = row['StockNameFormated']
    print(comp_name)
    ticker = row['TickerFormated']
    print(ticker)
    quarter = row['quarter']
    origin_page = f"https://news.alphastreet.com/{comp_name}-{ticker}-{quarter}-earnings-call-transcript/"
    print("getting page " + origin_page)
    driver.get(origin_page)
    driver.implicitly_wait(1)   
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    list_res = []
    alist = soup.find_all("div",{'class':'highlighter-content'})
    for i in range(len(alist)):
        list_res.append(alist[i].text)

    driver.quit()
    
    if len(list_res) > 0:
        list_res = list_res[0]
    else:
        list_res = np.nan
    
    return list_res


    
Stock_Tickers=pd.read_excel(filePath,sheet_name='Test')
years = [2022]
quarters = ["q1","q2","q3","q4"]
list_quarters =  [i + '-' + str(j) for i in quarters for j in years]
test = generate_df(Stock_Tickers[:10], list_quarters)

tqdm.pandas()
test['Transcript'] = test.progress_apply(process_page, axis = 1)


test = test.dropna()

test.to_csv("transcripts.csv", index = None)
