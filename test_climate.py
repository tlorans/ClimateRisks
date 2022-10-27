import os
import re
import time
import csv
import random
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from datetime import date, timedelta, datetime
from urllib.request import urlopen
import pandas as pd
import numpy as np
from time import sleep
from random import randint
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent



from climaterisks import transcript_collector
from climaterisks import stock_info_collector

import pandas as pd 

Stock_Tickers=pd.read_excel('Stoc_industries.xlsx',sheet_name='Test')
Stock_Tickers.iloc[0]["Description"]
transcript_collector.Get_Transcripts(Stock_Tickers)
dfContent=stock_info_collector.Get_from_Yahoo(Stock_Tickers)  


transcript_collector.Get_Transcripts(dfContent)

test = transcript_collector.process_page(dfContent.iloc[1])
print(str(test["Speech"]))

check = test["Speech"][0]
from climaterisks import earning_calls 

test = earning_calls.reformat(dfContent.iloc[0][1])
print(test)
