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


from climaterisks import earning_calls

#Reset list of URL's
correct_url = []
Url_list = []

#Reset Tables
ticker_data = []
company_data = []
title_data = []
date_data = []
time_data = []
quarter_data = []
company_info_table = []
Speech_table = []
QA_table = []
Comp_part_table = []
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


