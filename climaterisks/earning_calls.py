"""Main module."""

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
from pandera.typing import DataFrame, DateTime, Object, Series
import pandera as pa
import datetime

class CompanyInfoSchema(pa.SchemaModel):
    """Definition of a dataframe containing the company info schema"""

    CC_ID: Series[str]
    """Company ID"""
    Tickers: Series[str]
    """Tickers"""
    Company: Series[str]
    """Company name"""
    Call_Title: Series[str]
    """call title"""
    Fiscal_Quarter: Series[str]
    """FQ"""
    date: Series[Object]
    """date"""

class SpeechSchema(pa.SchemaModel):
    """Definition of a dataframe containing the earning call speech"""

    CC_ID: Series[str]
    """Company ID"""
    Script_ID: Series[str]
    """Id of the speech transcript"""
    Speech: Series[str]
    """Speech in string"""

class QASchema(pa.SchemaModel):
    """Definition of a dataframe containing the earning call QA"""

    CC_ID: Series[str]
    """Company ID"""
    Script_ID: Series[str]
    """Id of the speech transcript"""
    QA: Series[str]
    """QA in string"""


def pullpageurls(siteurl:str):
    Url_list = []
    pages = np.arange(150,200,1)
    driver = webdriver.Chrome('./chromedriver')
    #Pulling seeking alpha transcript search page
    for page in pages:
        page = siteurl+"/"+str(page)
        driver.get(page)
        site_html = driver.page_source
        soup_site = BeautifulSoup(site_html,'html.parser')
        sleep(random.randint(1,5))
        #Pulling transcript urls from seeking alpha transcript search page
        url_begin = 'https://seekingalpha.com'
        site_content = soup_site.find_all('h3')
        #Extracting url and placing into a list
        for url in site_content:
            url_pull = url.find('a',class_ = 'dashboard-article-link')
            partial_url = url_pull.get('href')
            pageURL = url_begin+partial_url
            Url_list.append(pageURL)
    return Url_list

def pullpagedetails(Url_list:list):
    driver = webdriver.Chrome('./chromedriver')
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}
    
    #Reset Tables
    ticker_data = []
    company_data = []
    title_data = []
    date_data = []
    time_data = []
    quarter_data = []
    company_info_table = []
    QA_table = []
    speech = []
    speaker = []
    QA_speech = []
    QA_speaker = []
    comp_parts = []
    comp_pos = []
    conf_parts = []
    conf_pos = []
    Conf_part_table = []
    comp_ccid = []
    speech_ccid = []
    QA_ccid = []
    comppart_ccid = []
    confpart_ccid = []
    speech_scriptid = []
    QA_scriptid = []
    comppart_partid = []
    confpart_partid = []
    test_list = []

    try:
        counter = company_info_table['CC ID'].iloc[-1] + 1
        counter2 = QA_table['Script ID'].iloc[-1] + 1
        counter3 = Conf_part_table['Part ID'].iloc[-1] + 1
    except:
        counter = 0
        counter2 = 0
        counter3 = 0
    for i in Url_list:
        if ('2020' in i or '2019'in i) and ('earnings' in i):
            #Pulling relevant information from URL's
            #Header to mimic browser visit
            #Create requests.models.response object from URL
            driver.get(i)
            html = driver.page_source
            #Create the soup
            soup = BeautifulSoup(html, "lxml")
            call = soup.find('div',id = 'content-rail')
            #Testing if URL contains necessary elements
            test_list = []
            test = call.find_all('p',class_ = re.compile('p p*'))
            for c in test:
                x = c.text.strip()
                test_list.append(x)
            if ('Operator' in test_list) and ('Conference Call Participants' in test_list):
                #Basic Company Info Section
                #Create cc_id
                cc_id = counter
                #Find company ticker
                try:
                    ticker = call.find('a',class_ = 'ticker-link').text.split(" ")[-1]
                    ticker_data.append(ticker)
                except:
                    ticker_data.append('None')
                #Find company name
                try:
                    company = call.find('a', class_ = 'ticker-link').text.split(" ")[0:-1]
                    company = " ".join(company)
                    company_data.append(company)
                except:
                    company_data.append('None')
                                #Find call title
                try:
                    title = call.find('h1').text
                    title_data.append(title)
                except:
                    title_data.append('None')
                #Find quarter/year
                try:
                    date_text = call.find('p',class_ = 'p p1').text.split(') ')[1]
                    quarter = date_text[0:7]
                    quarter_data.append(quarter)
                except:
                    quarter_data.append('None')
                #Find call date
                try:
                    date_string = date_text[date_text.index('Call')+5:].split("Call ")[0]
                    date = date_string[:date_string.index(":")-2].strip()
                    date_data.append(date)
                except:
                    date_data.append('None')
                #Find call time
                try:
                    time = date_string[date_string.index(":")-2:].strip()
                    time_data.append(time)
                except:
                    time_data.append('None')
                #Add CC ID
                comp_ccid.append(cc_id)
        #Speech and Company Participants Section
                bj = []
                indices = []
                convo = []
                #Pull speech script section
                script = call.find_all('p',class_ = re.compile('p p*'))
                #pull strong tags from speech script section
                for i in script:
                    if i.find('strong') is not None:
                        g = "strong"
                    else:
                        g = 0
                    bj.append(g)
                #Create list of index position of strong tags
                for j in range(len(bj)):
                    if bj[j] == 'strong':
                        indices.append(j)
                #Create list of text from speech script
                for k in script:
                    x = k.text.strip()
                    convo.append(x)
                #Create script ID & Participant ID
                script_id = counter2
                part_id = counter3
                #Create index objects to find positions of speech & participant sections
                conf_part_index = convo[convo.index('Conference Call Participants')+1:convo.index('Operator')]
                try:
                    speech_index = indices[0:indices.index(convo.index('Question-and-Answer Session'))]
                except:
                    speech_index = indices[0:indices.index(convo.index('Question-And-Answer Session'))]
                try:
                    QA_index = indices[indices.index(convo.index('Question-and-Answer Session'))+1:]
                except:
                    QA_index = indices[indices.index(convo.index('Question-And-Answer Session'))+1:]
                try:
                    comp_part_index = convo[convo.index('Company Participants')+1:convo.index('Conference Call Participants')]
                except:
                    comp_part_index = convo[convo.index('Corporate Participants')+1:convo.index('Conference Call Participants')]
                #Pulling info from speech section
                for i in range(2,len(speech_index)-1):
                    try:
                        z = convo[speech_index[i]+1:speech_index[i+1]]
                        speech.append(z)
                    except:
                        speech.append('None')
                    try:
                        g = convo[speech_index[i]]
                        speaker.append(g)
                    except:
                        speaker.append('None')
                    #Add CC ID & Script ID
                    speech_ccid.append(cc_id)
                    speech_scriptid.append(script_id)
                counter2 += 1
                script_id = counter2
                #Pulling info from Q&A section
                for i in range(0,len(QA_index)-1):
                    try:
                        q = convo[QA_index[i]+1:QA_index[i+1]]
                        QA_speech.append(q)
                    except:
                        QA_speech.append('None')
                    try:
                        f = convo[QA_index[i]]
                        QA_speaker.append(f)
                    except:
                        QA_speaker.append('None')
                    #Add CC ID & Script ID
                    QA_ccid.append(cc_id)
                    QA_scriptid.append(script_id)
                counter2 += 1
                script_id = counter2
                #Pulling company participants
                for i in comp_part_index:
                    x = i.split('-')
                    try:
                        a = x[0]
                        comp_parts.append(a)
                    except:
                        comp_parts.append('None')
                    try:
                        b = x[1]
                        comp_pos.append(b)
                    except:
                        comp_pos.append('None')
                    #Add CC ID & Part ID
                    comppart_ccid.append(cc_id)
                    comppart_partid.append(part_id)
                    counter3 += 1
                    part_id = counter3
                #Pulling conference participants
                for i in conf_part_index:
                    x = i.split('-')
                    try:
                        a = x[0]
                        conf_parts.append(a)
                    except:
                        conf_parts.append('None')
                    try:
                        b = x[1]
                        conf_pos.append(b)
                    except:
                        conf_pos.append('None')
                    #Add CC ID & Part ID
                    confpart_ccid.append(cc_id)
                    confpart_partid.append(part_id)
                    counter3 += 1
                    part_id = counter3
                #Add to CC ID
                counter += 1
            else:
                continue
        #Pause in between trying each call transcript
        sleep(random.randint(1,2))