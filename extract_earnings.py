# -*- coding: utf-8 -*-
"""
Created on Mon Jan  2 09:17:01 2023

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

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
service = Service(executable_path=ChromeDriverManager().install())

def get_yahoo_longname(symbol):
    response = urllib.request.urlopen(f'https://query2.finance.yahoo.com/v1/finance/search?q={symbol}')
    content = response.read()
    data = json.loads(content.decode('utf8'))['quotes'][0]['longname']
    return data

def Get_from_Yahoo(Stock_Tickers:DataFrame) -> DataFrame:   
    dfContent = pd.DataFrame(columns=['StockIndex', 'StockName'])
    for i in range(len(Stock_Tickers)):
        print(Stock_Tickers['Symbol'][i])
        try:
            long_name = get_yahoo_longname(Stock_Tickers['Symbol'][i])
            dfContent = dfContent.append({'StockIndex': Stock_Tickers['Symbol'][i], 
                                          'StockName': long_name
                                          },ignore_index=True )           
        except:
                print("Error in " +str(Stock_Tickers['Symbol'][i])) 
    
    dfContent['StockName'] = dfContent['StockName'].apply(lambda x : x.replace(',', ''))
    dfContent['StockName'] = dfContent['StockName'].apply(lambda x : x.replace('.', ''))
    return dfContent



def reformat(text:str) -> str:
    text=text.lower() 
    text=re.sub("\\W"," ",text) # remove special chars
    words=re.split("\\s+",text)
    # stem words
    words = [word for word in words if word != ""]
    return "-".join(words)

def process_page(StockTicker, quarter:str):    
    driver = webdriver.Chrome(service=service,chrome_options=chrome_options)
    comp_name = str(reformat(StockTicker["StockName"]))
    print(comp_name)
    ticker = str(reformat(StockTicker["StockIndex"]))
    print(ticker)
    origin_page = f"https://news.alphastreet.com/{comp_name}-{ticker}-{quarter}-earnings-call-transcript/"
    print("getting page " + origin_page)
    driver.get(origin_page)
    driver.implicitly_wait(100)   
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    list_res = []
    alist = soup.find_all("div",{'class':'highlighter-content'})
    for i in range(len(alist)):
        list_res.append(alist[i].text)

    driver.quit()
    df = pd.DataFrame({"StockIndex":StockTicker["StockName"], 
                        "StockName":StockTicker["StockIndex"],
                        "quarter":quarter,
                        "Speech":list_res})
    return df



def process_page_alt(StockTicker, quarter:str):    
    driver = webdriver.Chrome(service=service,chrome_options=chrome_options)
    comp_name = str(reformat(StockTicker["StockName"]))
    print(comp_name)
    ticker = str(reformat(StockTicker["StockIndex"]))
    print(ticker)
    origin_page = f"https://news.alphastreet.com/{comp_name}-{ticker}-{quarter}-earnings-conference-call-transcript/"
    print("getting page " + origin_page)
    driver.get(origin_page)
    driver.implicitly_wait(100)   
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    list_res = []
    alist = soup.find_all("div",{'class':'highlighter-content'})
    for i in range(len(alist)):
        list_res.append(alist[i].text)

    driver.quit()
    df = pd.DataFrame({"StockIndex":StockTicker["StockName"], 
                        "StockName":StockTicker["StockIndex"],
                        "quarter":quarter,
                        "Speech":list_res})
    return df



def get_transcripts(Stock_Tickers:DataFrame) -> DataFrame:
    quarters = ["q1","q2","q3","q4"]
    years = [2020,2021,2022]
    list_quarters =  [i + '-' + str(j) for i in quarters for j in years]

    df = pd.DataFrame()
    for i in tqdm(range(len(Stock_Tickers))):
        for j in range(len(list_quarters)):
            print("******Getting Transcripts for:"+ str(Stock_Tickers['StockIndex'][i]))
            new_df = process_page(Stock_Tickers.iloc[i], list_quarters[j])
            if new_df.shape[0] < 1:
                new_df = process_page_alt(Stock_Tickers.iloc[i], list_quarters[j])
            df = pd.concat([df, new_df])
    print('All targeted transcripts done.') 
    return df

def get_earning_calls(filePath) -> DataFrame:
    Stock_Tickers=pd.read_excel(filePath,sheet_name='Test')
    dfContent= Get_from_Yahoo(Stock_Tickers)  
    results = get_transcripts(dfContent)
    return results 


import urllib



test = get_earning_calls('materials/Stoc_industries.xlsx')

Stock_Tickers=pd.read_excel('materials/Stoc_industries.xlsx',sheet_name='Test')

dfContent = Get_from_Yahoo(Stock_Tickers)

dfContentsub = dfContent[dfContent['StockIndex'] == 'TSLA']

quarters = ["q1","q2","q3","q4"]
years = [2022]
list_quarters =  [i + '-' + str(j) for i in quarters for j in years]

df = pd.DataFrame()
for i in tqdm(range(len(dfContentsub))):
    for j in range(len(list_quarters)):
        print("******Getting Transcripts for:"+ str(dfContentsub['StockIndex'][i]))
        new_df = process_page(dfContentsub.iloc[i], list_quarters[j])
        df = pd.concat([df, new_df])

dfContentsub['StockIndex']
