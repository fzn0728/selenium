# -*- coding: utf-8 -*-
"""
Created on Thu Dec 15 09:41:47 2016

@author: ZFang
"""


from bs4 import BeautifulSoup
from urllib.request import urlopen
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import time
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from fredapi import Fred
from datetime import datetime, timedelta
import dateutil.relativedelta
import numpy as np
import json




def setup_driver():
    binary = FirefoxBinary('C:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe')
    driver = webdriver.Firefox(firefox_binary=binary)
    return driver  

def open_russell(url):
    # Set up the driver
    driver = setup_driver()
    # Open the russell and manipulate the website
    driver.get(url)
    login = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, "lazy"))).click()  
    time.sleep(5)
    driver.switch_to_window(driver.window_handles[-1])
    # Page 1
    driver.find_element_by_xpath("//input[@name='FundCode'][@value='irs3']").click()
    driver.find_element_by_xpath("//input[@name='FundCode'][@value='iru2']").click()
    driver.find_element_by_xpath("//input[@name='FundCode'][@value='irus']").click()
    driver.find_element_by_css_selector("a[href='javascript:submitForm(document.forms[0].action);']").submit()
    # Page 2
    time.sleep(5)
    driver.find_element_by_xpath("//input[@id='rdoStdRtrn'][@value='standard']").click()
    driver.find_element_by_css_selector("a[href='javascript:submitForm(document.forms[0].action);']").submit()
    # Page 3
    time.sleep(5)
    driver.find_element_by_xpath("//input[@name='IndividualTimeFreq'][@value='1_day']").click()
    driver.find_element_by_xpath("//input[@name='IndividualTimeFreq'][@value='Last_3_mo']").click()
    driver.find_element_by_xpath("//input[@name='IndividualTimeFreq'][@value='1_year']").click()
    driver.find_element_by_xpath("//input[@name='IndividualTimeFreq'][@value='3_years']").click()
    driver.find_element_by_xpath("//input[@name='IndividualTimeFreq'][@value='5_years']").click()
    driver.find_element_by_xpath("//input[@name='IndividualTimeFreq'][@value='10_years']").click()
    driver.find_element_by_xpath("//input[@name='IndividualTimeFreq'][@value='MTD']").click()
    driver.find_element_by_xpath("//input[@name='IndividualTimeFreq'][@value='QTD']").click()
    driver.find_element_by_xpath("//input[@name='IndividualTimeFreq'][@value='YTD']").click()
    time.sleep(5)
    driver.find_element_by_xpath("//input[@name='IndividualTimeFreq'][@value='MTD']").click()
    driver.find_element_by_xpath("//input[@name='IndividualTimeFreq'][@value='QTD']").click()
    driver.find_element_by_xpath("//input[@name='IndividualTimeFreq'][@value='YTD']").click()
    # Select date on Page 3
    time.sleep(5)
    # driver.find_element_by_xpath("//select[@name='d_startDate']/option[@value='12']").submit()
    # Click Next on Page 3
    driver.find_element_by_css_selector("a[href='javascript:validateForm(document.forms[0].action);']").click() 
    return driver

def HFRX_get_value(url_hfrx):
    # Set up the driver
    driver = setup_driver()
    # Open the website
    driver.get(url_hfrx)
    
    try:
        if driver.find_element_by_name("login").is_displayed:
            driver.find_element_by_name("login").click()
    except:
        pass
    time.sleep(5)
    
    soup = BeautifulSoup(driver.page_source,'lxml')
    # Get the text content of current website
    table = soup.find_all('div',attrs={'class':'data-table-wrapper'})
    data = []
    for t_ in table:
        rows = t_.find_all('tr')
        for r_ in rows:
            cols = r_.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            data.append([ele for ele in cols if ele])
    df = pd.DataFrame([part for part in data])
    if len(df) == 10:
        df.columns = ['Index Name','DTD','MTD','YTD','Index Value','Recent Month_1','Recent Month_2','YTD','Last 12M','Last 36M']
    elif len(df) == 9:
        df.columns = ['Index Name','DTD','MTD','YTD','Index Value','Recent Month_1','YTD','Last 12M','Last 36M']
    return df
    
def Russell_get_value(url_russell):
    # Set up the driver
    driver = setup_driver()
    # Open the website
    driver = open_russell(url_russell)
    # Get the text content of current website
    time.sleep(5)
    content = driver.page_source
    soup =  BeautifulSoup(content,"lxml")
    table = soup.find_all('tr', attrs={'bgcolor':'#FFFFFF'})
    data = []
    for t_ in table:
        rows = t_.find_all('td')
        rows = [ele.text.strip() for ele in rows]
        data.append([ele for ele in rows if ele]) # Get rid of empty values 
    df = pd.DataFrame([part for part in data])    
    return df
    
def MSCI_get_value(url_table,MKT):
    '''
    Find 'tbody' first, and locate the 'tr' tag, then extract all text after 'td' tag.
    '''
    # Get soup
    soup = BeautifulSoup(urlopen(url_table).read(),'lxml')
    # Get data value
    # Fetch html from url (jsf in this case)
    # Parse raw data from the table 
    data = []
    table = soup.find("tbody", id = "templateForm:tableResult0:tbody_element")
    rows = table.find_all('tr')
    for tr in rows:
        cols = tr.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele]) # Get rid of empty values    
    # Clean the format and change it into dataframe
    df = pd.DataFrame([part for part in data])
    df.columns=['MSCI Index','Index name','Last','Day','MTD','QTD','YTD','1 Yr','3 Yr','5 Yr','10 Yr']
    df.to_csv('MSCI_%s.csv'%MKT)
    return df

def SP_DJI_get_value(url_sp):
    # Set up the driver
    driver = setup_driver()
    # Open the website
    driver.get(url_sp)
    time.sleep(10)
    driver.find_element_by_class_name('table ').click()
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source,'lxml')    
    table = soup.find('table',attrs={'class':'daily-return-table'})
    rows = table.find_all('tr')
    data = []
    for t_ in rows:
        cols = t_.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele])
    df = pd.DataFrame([part for part in data])
    df.columns = ['Index name','Index Level','1 Day','MTD','QTD','YTD']
    return df

def Bond_get_value():
    
    fred = Fred(api_key='a0718ea00e6784c5f8b452741622a98c')
    current_date = datetime.today() - timedelta(days=1)
    one_month_delta = datetime.today() - dateutil.relativedelta.relativedelta(months=1)
    three_month_delta = datetime.today() - dateutil.relativedelta.relativedelta(months=3)
    six_month_delta = datetime.today() - dateutil.relativedelta.relativedelta(months=6)
    twelve_month_delta = datetime.today() - dateutil.relativedelta.relativedelta(months=12)
    # today = current_date.strftime('%m/%d/%Y')
    
    
    def find_closest_data(product,date):
        i = 1
        Treasury_df = pd.DataFrame(fred.get_series(product,observation_start=date))
        while len(Treasury_df)==0:
            new_date = date - timedelta(days=i+1)
            Treasury_df = pd.DataFrame(fred.get_series(product,observation_start=new_date))
        else:
            pass
        return Treasury_df
    
    ### Get value
    Treasury_10Y = find_closest_data('DGS10',current_date)
    Treasury_10_1M = pd.DataFrame(fred.get_series('DGS10',observation_start=one_month_delta))
    Treasury_10_3M = pd.DataFrame(fred.get_series('DGS10',observation_start=three_month_delta))
    Treasury_10_6M = pd.DataFrame(fred.get_series('DGS10',observation_start=six_month_delta))
    Treasury_10_12M = pd.DataFrame(fred.get_series('DGS10',observation_start=twelve_month_delta))
    
    Treasury_30Y = find_closest_data('DGS10',current_date)
    Treasury_30_1M = pd.DataFrame(fred.get_series('DGS30',observation_start=one_month_delta))
    Treasury_30_3M = pd.DataFrame(fred.get_series('DGS30',observation_start=three_month_delta))
    Treasury_30_6M = pd.DataFrame(fred.get_series('DGS30',observation_start=six_month_delta))
    Treasury_30_12M = pd.DataFrame(fred.get_series('DGS30',observation_start=twelve_month_delta))
    
    
    # Collect them into the dataframe
    Bond_Yield_df = pd.DataFrame(np.zeros([4,5]),columns=['Yield','MTD','3 Month','6 Month','1 Year'],index=['10-Year Treasury Note','30-Year Treasury Note','10-Year AA Corporates','20-Year AA Corporates'])
    Bond_Yield_df.iloc[0,0] = Treasury_10Y.iloc[0,0]
    Bond_Yield_df.iloc[0,1] = Treasury_10_1M.iloc[0,0]
    Bond_Yield_df.iloc[0,2] = Treasury_10_3M.iloc[0,0]
    Bond_Yield_df.iloc[0,3] = Treasury_10_6M.iloc[0,0]
    Bond_Yield_df.iloc[0,4] = Treasury_10_12M.iloc[0,0]

    Bond_Yield_df.iloc[1,0] = Treasury_30Y.iloc[0,0]
    Bond_Yield_df.iloc[1,1] = Treasury_30_1M.iloc[0,0]
    Bond_Yield_df.iloc[1,2] = Treasury_30_3M.iloc[0,0]
    Bond_Yield_df.iloc[1,3] = Treasury_30_6M.iloc[0,0]
    Bond_Yield_df.iloc[1,4] = Treasury_30_12M.iloc[0,0]

    return Bond_Yield_df
def currency_get_data(date):
    
    url = "http://api.fixer.io/%s?base=USD"%date
    response = urlopen(url)
    data = json.loads(response.read().decode(response.info().get_param('charset') or 'utf-8'))
    return data
def currency_get_value():
    current_date = datetime.today() - timedelta(days=1)
    one_month_delta = datetime.today() - dateutil.relativedelta.relativedelta(months=1)
    three_month_delta = datetime.today() - dateutil.relativedelta.relativedelta(months=3)
    six_month_delta = datetime.today() - dateutil.relativedelta.relativedelta(months=6)
    twelve_month_delta = datetime.today() - dateutil.relativedelta.relativedelta(months=12)
    
    current_date = current_date.strftime('%Y-%m-%d')
    one_month_delta = one_month_delta.strftime('%Y-%m-%d')
    three_month_delta = three_month_delta.strftime('%Y-%m-%d')
    six_month_delta = six_month_delta.strftime('%Y-%m-%d')
    twelve_month_delta = twelve_month_delta.strftime('%Y-%m-%d')
    
    
    Currency_df = pd.DataFrame(np.zeros([3,5]),columns=['Spot','MTD','3 Month Change','6 Month Change','1 Year Change'],index=['USD/GBP','USD/EUR','JPY/USD'])
    
    
    data_c = currency_get_data(current_date)
    Currency_df.iloc[0,0]=1/data_c['rates']['GBP']
    Currency_df.iloc[1,0]=1/data_c['rates']['EUR']
    Currency_df.iloc[2,0]=data_c['rates']['JPY']
    
    data_one = currency_get_data(one_month_delta)
    Currency_df.iloc[0,1]=(1/data_one['rates']['GBP']-Currency_df.iloc[0,0])/Currency_df.iloc[0,0]
    Currency_df.iloc[1,1]=(1/data_one['rates']['EUR']-Currency_df.iloc[1,0])/Currency_df.iloc[1,0]
    Currency_df.iloc[2,1]=(data_one['rates']['JPY']-Currency_df.iloc[2,0])/Currency_df.iloc[2,0]
    
    data_three = currency_get_data(three_month_delta)
    Currency_df.iloc[0,2]=(1/data_three['rates']['GBP']-Currency_df.iloc[0,0])/Currency_df.iloc[0,0]
    Currency_df.iloc[1,2]=(1/data_three['rates']['EUR']-Currency_df.iloc[1,0])/Currency_df.iloc[1,0]
    Currency_df.iloc[2,2]=(data_three['rates']['JPY']-Currency_df.iloc[2,0])/Currency_df.iloc[2,0]
    
    data_six = currency_get_data(six_month_delta)
    Currency_df.iloc[0,3]=(1/data_six['rates']['GBP']-Currency_df.iloc[0,0])/Currency_df.iloc[0,0]
    Currency_df.iloc[1,3]=(1/data_six['rates']['EUR']-Currency_df.iloc[2,0])/Currency_df.iloc[2,0]
    Currency_df.iloc[2,3]=(data_six['rates']['JPY']-Currency_df.iloc[2,0])/Currency_df.iloc[2,0]
    
    data_twe = currency_get_data(twelve_month_delta)
    Currency_df.iloc[0,4]=(1/data_twe['rates']['GBP']-Currency_df.iloc[0,0])/Currency_df.iloc[0,0]
    Currency_df.iloc[1,4]=(1/data_twe['rates']['EUR']-Currency_df.iloc[2,0])/Currency_df.iloc[2,0]
    Currency_df.iloc[2,4]=(data_twe['rates']['JPY']-Currency_df.iloc[2,0])/Currency_df.iloc[2,0]    
   
    return  Currency_df
    
def multiple_sheets(df_list, file_name):
    '''This function could put rolling dataframe into different sheets within a single excel file
    
    Args:
        df_list is the list of all dataframe
        file_name is the name of excel file
    '''
    # d = {}
    writer = pd.ExcelWriter(file_name, engine = 'xlsxwriter')
    workbook  = writer.book
    # Initial Format
    # format1 = workbook.add_format({'num_format': '#,###0.000'})
    # format1.set_align('center')
    # format2 = workbook.add_format({'num_format': '0.00%'})  
    # format2.set_align('center')
    # format3 = workbook.add_format({'num_format': 'General'})
    # format3.set_align('center')
    # format4 = workbook.add_format({'num_format': 'General'})
    # format4.set_align('center')
    # format4.set_bold()
    # format4.set_border()
    # format5 = workbook.add_format({'num_format': '#,###0.000'})
    # format5.set_align('center')
    # format5.set_border()
    # Paste dataframe
    for dataframe in df_list:
        dataframe.to_excel(writer, '%s' %dataframe.name)
        # d["{0}".format(dataframe)] = writer.sheets[dataframe.name]
        # d[dataframe].set_column('A:A', 35, format3)
        # d[dataframe].set_column('B:B', 18, format1)
        # d[dataframe].set_column('C:C', 18, format1)
        # d[dataframe].set_column('D:D', 18, format1)
        writer.sheets[dataframe.name].set_column('A:A', 26)
        writer.sheets[dataframe.name].set_column('B:B', 23)
        writer.sheets[dataframe.name].set_column('C:C', 23)
        writer.sheets[dataframe.name].set_column('D:D', 23)
        writer.sheets[dataframe.name].set_column('E:E', 23)
        
    writer.save()  

if __name__ == '__main__':
    ###### Find urls ######
    url_hfrx = 'https://www.hedgefundresearch.com/family-indices/hfrx'
    url_russell = "http://www.ftserussell.com/tools-analytics/russell-index-performance-calculator"
    # Get the hidden link
    hidden_link_DM = 'https://app2.msci.com/webapp/indexperf/pages/IEIPerformanceRegional.jsf'
    hidden_link_EM = 'https://app2.msci.com/webapp/indexperf/pages/IEIPerformanceRegional.jsf'
    url_sp = 'http://us.spindices.com/indices/equity/sp-500'
    url_dji = 'http://us.spindices.com/indices/equity/dow-jones-industrial-average'
    ###### HFRX Index ######
    df_HFRX = HFRX_get_value(url_hfrx)
    su_HFRX = df_HFRX.iloc[[1,7,17,25,36],[0,2,3]]
    su_HFRX.name = 'Hedge Funds'
    ###### Russell Index ######
    df_Russell = Russell_get_value(url_russell)
    su_Russell = df_Russell.iloc[[3,5,7],[0,1,2,3]]
    su_Russell.columns = df_Russell.iloc[0,:]

    ###### MSCI Index ######
    ### link = find_hidden_link(url)
    df_MSCI_DM = MSCI_get_value(hidden_link_DM,'DM')
    df_MSCI_EM = MSCI_get_value(hidden_link_EM,'EM')
    su_MSCI = df_MSCI_DM.iloc[[31],[1,4,5,6]]
    su_MSCI.iloc[0,0] = 'MSCI World-Ex US'
    
    
    ###### S&P500 Index ######
    df_SP = SP_DJI_get_value(url_sp)
    su_SP = df_SP.iloc[[6],[0,3,4,5]]

    ###### DJI Index ######
    df_DJI = SP_DJI_get_value(url_dji)
    su_DJI = df_DJI.iloc[[6],[0,3,4,5]]

    ###### Treasury Curve ######
    su_Bond = Bond_get_value()
    su_Bond.name = ''
    
    ###### Currency ######
    su_Currency = currency_get_value()
    su_Currency.name = 'FX Rates'
    
    # Conpact the dataframe
    su_Euqity = pd.concat([su_Russell,su_MSCI,su_SP,su_DJI],axis=0)
    su_Euqity.name = 'Euiqty Indices'
    
    ###### Output ######
    multiple_sheets([su_HFRX, su_Euqity,su_Bond,su_Currency],'test_output.xlsx')