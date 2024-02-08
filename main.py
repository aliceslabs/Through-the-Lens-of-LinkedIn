#import everything we will need
import time
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

#make web instance
from selenium.webdriver.common.by import By

browser = webdriver.Chrome()

#open and log into linkedin
browser.get("https://www.linkedin.com/login/")
file = open("config.txt")
line = file.readlines()
username = line[0]
password = line[1]
eID = browser.find_element(By.ID, 'username')
eID.send_keys(username)
eID = browser.find_element(By.ID, 'password')
eID.send_keys(password)
browser.get('https://www.linkedin.com/school/queen\'s-university/people/')
browser.execute_script('window.scrollTo(5000, document.body.scrollHeight);')
time.sleep(5)
eID = browser.find_element(By.XPATH, '//button[@aria-label="Next"]')
eID.click()
eID = browser.find_element(By.XPATH, '//button[@aria-label="Next"]')
eID.click()
eID = browser.find_element(By.XPATH, '//button[@aria-label="Next"]')
eID.click()
eID = browser.find_element(By.XPATH, '//button[@aria-label="Show more people filters"')
eID.click()
eID = browser.find_element(By.NAME, "Computer Science")
eID.click()
# change depending on how much we must scroll
repetitions = 50 
last_height = browser.execute_script("return document.body.scrollHeight")
for i in range(repetitions):
  browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
  time.sleep(5)
  new_height = browser.execute_script("return document.body.scrollHeight")
  if new_height == last_height:
    break
  new_height = last_height
