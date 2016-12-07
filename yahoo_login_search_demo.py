# -*- coding: utf-8 -*-
"""
Created on Tue Dec  6 14:00:19 2016

@author: ZFang
"""

import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

if __name__ == "__main__":
    binary = FirefoxBinary('C:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe')
    driver = webdriver.Firefox(firefox_binary=binary)
    
    driver.get("https://finance.yahoo.com/")
    login = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "uh-signedin")))    
    
    # login = driver.find_element_by_id("uh-signedin")
    login.send_keys(Keys.RETURN)
    assert "No results found." not in driver.page_source
    
    username = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.NAME, "username")))
    # username = driver.find_element_by_name("username")
    username.send_keys("thames.ft@gmail.com")
    username.send_keys(Keys.RETURN)
    
    time.sleep(10)
    password = driver.find_element_by_name("passwd")
    password.send_keys("fzn07285612289")
    password.send_keys(Keys.RETURN)
    
    search = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.NAME, "p")))
    # search = driver.find_element_by_name("p")
    search.send_keys('AAPL')
    time.sleep(3)
    search.send_keys(Keys.RETURN)
    driver.close()
