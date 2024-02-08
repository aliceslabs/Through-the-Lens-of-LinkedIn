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
