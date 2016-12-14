

import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests

if __name__ == "__main__":
    binary = FirefoxBinary('C:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe')
    driver = webdriver.Firefox(firefox_binary=binary)
    
    driver.get("http://www.ftserussell.com/tools-analytics/russell-index-performance-calculator")
    login = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, "lazy"))).click()  
    time.sleep(5)
    driver.switch_to_window(driver.window_handles[-1])
    #Page 1
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
#    driver.find_element_by_xpath("//select[@name='m_startDate']/option[@value='12']").click()
    driver.find_element_by_xpath("//select[@name='d_startDate']/option[@value='12']").submit()
#    driver.find_element_by_xpath("//select[@name='y_startDate']/option[@value='2016']").click()
    # Click Next on Page 3
    driver.find_element_by_css_selector("a[href='javascript:validateForm(document.forms[0].action);']").click()
    # 
    
    # MSCI Data
    
    
    
    
    
#    driver.find_element_by_name("FundCode").click()
#    yesRadioButton.Click();
    # login = driver.find_element_by_id("uh-signedin")
#    login.send_keys(Keys.RETURN)
#    assert "No results found." not in driver.page_source
#    
#    username = WebDriverWait(driver, 20).until(
#        EC.presence_of_element_located((By.NAME, "username")))
#    # username = driver.find_element_by_name("username")
#    username.send_keys("thames.ft@gmail.com")
#    username.send_keys(Keys.RETURN)
#    
#    time.sleep(10)
#    password = driver.find_element_by_name("passwd")
#    password.send_keys("fzn07285612289")
#    password.send_keys(Keys.RETURN)
#    
#    search = WebDriverWait(driver, 20).until(
#        EC.presence_of_element_located((By.NAME, "p")))
#    # search = driver.find_element_by_name("p")
#    search.send_keys('AAPL')
#    time.sleep(3)
#    search.send_keys(Keys.RETURN)
#    driver.close()
