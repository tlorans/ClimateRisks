# -*- coding: utf-8 -*-
"""Get description of stocks based on ticker details
"""

from selenium import webdriver
import requests
import time
from bs4 import BeautifulSoup
import os
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.interaction import KEY
from selenium.webdriver.common import keys
import json
import yfinance as yf
from typing import Any, Dict, List, Optional
from pandera.typing import DataFrame, DateTime, Object, Series
import pandera as pa


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

def grab_page(url:str,company_ticker:str,company_name:str,dfContent:DataFrame) -> DataFrame:
    #Chrome Session
    #driver=webdriver.Chrome()
    driver = webdriver.Chrome('chromedriver',chrome_options=chrome_options)
    driver.get(url)
    driver.implicitly_wait(100)
    print("attempting to grab page: " + url)
    # page = requests.get(url)
    # page_html = page.text
    #soup = BeautifulSoup(page_html, 'html.parser')
     
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    content_Sector = soup.find("td", text="Sector:").find_next_sibling("td").text
    content_Industry=soup.find("td", text="Industry:").find_next_sibling("td").text
    driver.quit()
    dfContent = dfContent.append({'StockIndex': company_ticker, 
                                  'StockName': company_name,
                                  'Sector': content_Sector,
                                  'Industry':content_Industry
                                  },ignore_index=True)
    return dfContent
    

def Get_from_Yahoo(Stock_Tickers:DataFrame) -> DataFrame:   
    dfContent = pd.DataFrame(columns=['StockIndex', 'StockName','Sector', 'Industry'])
    for i in range(len(Stock_Tickers)):
        print(Stock_Tickers['Symbol'][i])
        try:
            ticker = yf.Ticker(Stock_Tickers['Symbol'][i])
            dfContent = dfContent.append({'StockIndex': Stock_Tickers['Symbol'][i], 
                                          'StockName': ticker.info['longName'],
                                          'Sector': ticker.info['sector'],
                                          'Industry':ticker.info['industry']
                                          },ignore_index=True )           
        except:
                print("Error in " +str(Stock_Tickers['Symbol'][i])) 
    
    return dfContent

