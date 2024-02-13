import time
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import pandas as pd
import csv
import os
import re
import random

OUTPUT_CSV_FILENAME = 'profiles.csv'
THIS_YEAR = 2024

if not os.path.exists(OUTPUT_CSV_FILENAME):
    open(OUTPUT_CSV_FILENAME, 'w').close()
if os.stat(OUTPUT_CSV_FILENAME).st_size == 0:
    # write the file header
    with open(OUTPUT_CSV_FILENAME, 'w', newline='\n', encoding='utf-8') as fp:
        writer = csv.writer(fp)
        writer.writerow(['username', 'name', 'location', 'graduation year', 'company', 'job title', 'skills'])

# get the existing usernames
existing_usernames = set(pd.read_csv(OUTPUT_CSV_FILENAME)['username'])

# browser instance
browser = webdriver.Chrome()

# read in popular names from the file
popular_names = []
with open('names.txt', 'r') as fp:
    for line in fp:
        popular_names.append(line.strip())


# login
def login():
    browser.get("https://www.linkedin.com/login/")
    file = open("config.txt")
    line = file.readlines()
    username = line[0]
    password = line[1]
    eID = browser.find_element(By.ID, 'username')
    eID.send_keys(username)
    eID = browser.find_element(By.ID, 'password')
    eID.send_keys(password)
    time.sleep(3)


# extract usernames
def extract_usernames(html_src):
    # BeautifulSoup instance
    soup = BeautifulSoup(html_src, 'html.parser')
    # get links
    usernames = []
    for li in soup.find_all('li', class_='reusable-search__result-container'):
        item = li.find('a', class_='app-aware-link')
        if item is None:
            continue
        link = item['href']
        if link.startswith('https://www.linkedin.com/search'):
            continue
        # get link
        username = link[28:].split('?')[0]
        usernames.append(username)
    return usernames


# get the name and location
def extract_name_location(html_src):
    soup = BeautifulSoup(html_src, 'html.parser')
    div = soup.find('div', class_='ph5 pb5')
    if div is None:
        return
    h1 = div.find('h1')
    if h1 is None:
        return
    # name
    name = h1.text.strip()

    span = div.find('span', class_='text-body-small inline t-black--light break-words')
    if span is None:
        return
    # location
    location = span.text.strip()

    return name, location


# get graduation year if the person is a Queen’s Computing Alumni
def extract_graduation_year(html_src):
    soup = BeautifulSoup(html_src, 'html.parser')
    div = soup.find('div', class_='scaffold-finite-scroll__content')
    if div is None:
        return
    for li in div.find_all('li'):
        # university
        item = li.find('div', class_='display-flex align-items-center mr1 hoverable-link-text t-bold')
        if item is None:
            continue
        university_name = item.find('span').text.strip()
        if university_name != "Queen's University":
            continue
        # major
        item = li.find('span', class_='t-14 t-normal')
        if item is None:
            break
        major = item.find('span').text.strip().lower()
        if 'computer' not in major or 'computing' in major:
            break
        # period
        item = li.find('span', class_='t-14 t-normal t-black--light')
        if item is None:
            return ''
        period = item.find('span').text.strip()
        graduation_year = int(re.findall(r'\d+', period)[-1])
        if graduation_year >= THIS_YEAR:
            return

        return graduation_year

    return


# get the company and job title
def extract_company_job_title(html_src):
    soup = BeautifulSoup(html_src, 'html.parser')
    div = soup.find('div', class_='scaffold-finite-scroll__content')
    if div is None:
        return
    li = div.find('li')
    if li is None:
        return

    div = li.find_all('div', class_='scaffold-finite-scroll__content')
    if len(div) == 0:
        # job title
        item = li.find('div', class_='display-flex align-items-center mr1 t-bold')
        if item is None:
            return
        job_title = item.find('span').text.strip()
        # company
        item = li.find('span', class_='t-14 t-normal')
        if item is None:
            return
        items = item.find('span').text.strip().split('·')[:-1]
        company = '.'.join(items).strip()
    else:
        item = li.find('div', class_='display-flex align-items-center mr1 hoverable-link-text t-bold')
        if item is None:
            return
        company = item.find('span').text.strip()
        item = div[0].find('div', class_='display-flex align-items-center mr1 hoverable-link-text t-bold')
        if item is None:
            return
        job_title = item.find('span').text.strip()

    return company, job_title


# get the skills
def extract_skills(html_src):
    soup = BeautifulSoup(html_src, 'html.parser')
    div = soup.find('div', class_='scaffold-finite-scroll__content')
    if div is None:
        return

    candidate_skills = {}
    for li in div.find_all('li'):
        item = li.find('div', class_='display-flex align-items-center mr1 hoverable-link-text t-bold')
        if item is None:
            continue
        # skill name
        skill_name = item.find('span').text.strip()
        # endorsements
        items = li.find_all('li', class_='dnNirAnNFXKvQsoHaZYhMCYLVWgPJxHGxmWk')
        if len(items) == 0:
            continue
        item = items[-1].find('div', class_='hoverable-link-text display-flex align-items-center t-14 t-normal t-black')
        if item is None:
            endorsements = 0
        else:
            numbers = re.findall(r'\d+', item.find('span').text.strip())
            if len(numbers) == 0:
                endorsements = 0
            else:
                endorsements = int(numbers[0])
        candidate_skills[skill_name] = endorsements

    # sort the candidate skills by the number of endorsements
    # then get the first five skills
    skills = list(map(lambda x: x[0], sorted(candidate_skills.items(), key=lambda x: x[1], reverse=True)))[:5]

    return ';'.join(skills)


# write one profile to the csv file
def write_one_profile(profile):
    global existing_usernames
    with open(OUTPUT_CSV_FILENAME, 'a', newline='\n', encoding='utf-8') as fp:
        writer = csv.writer(fp)
        writer.writerow(profile)

    existing_usernames.add(profile[0])


# extract profile information
def extract_profile(username):
    # skip duplicate usernames
    if username in existing_usernames:
        return

    profile_link = 'https://www.linkedin.com/in/%s/' % username
    experience_link = 'https://www.linkedin.com/in/%s/details/experience/' % username
    education_link = 'https://www.linkedin.com/in/%s/details/education/' % username
    skills_link = 'https://www.linkedin.com/in/%s/details/skills/' % username

    # get the name and location
    browser.get(profile_link)
    time.sleep(random.randint(2, 5))
    items = extract_name_location(browser.page_source)
    if items is None:
        return
    name, location = items[0], items[1]

    # get graduation year if the person is a Queen’s Computing Alumni
    browser.get(education_link)
    time.sleep(random.randint(2, 5))
    graduation_year = extract_graduation_year(browser.page_source)
    if graduation_year is None:
        return

    print('%s#%s#%s' % (name, location, graduation_year))

    # get the company and job title
    browser.get(experience_link)
    time.sleep(random.randint(2, 5))
    items = extract_company_job_title(browser.page_source)
    if items is None:
        company, job_title = '', ''
    else:
        company, job_title = items[0], items[1]

    # get the skills
    browser.get(skills_link)
    time.sleep(random.randint(2, 5))
    skills = extract_skills(browser.page_source)

    # write one profile to the csv file
    profile = [username, name, location, graduation_year, company, job_title, skills]
    write_one_profile(profile)


# crawl the user files
def crawl_user_files():
    for name in popular_names:
        print('Search name: %s' % name)
        page = 0
        while True:
            page = page + 1
            print('#page %d' % page)
            search_link = 'https://www.linkedin.com/search/results/people/?keywords=queen%27s%20university%20' + name + \
                          '%20computer%20science&network=%5B%22O%22%5D&origin=FACETED_SEARCH&profileLanguage=%5B%22en%22%5D&schoolFilter=%5B%226926%22%5D&page=' + \
                          str(page)
            browser.get(search_link)
            time.sleep(random.randint(2, 4))

            # extract usernames
            usernames = extract_usernames(browser.page_source)
            if len(usernames) == 0:
                break

            for username in usernames:
                # extract profile information
                extract_profile(username)

            time.sleep(random.randint(3, 5))

        print()
        time.sleep(random.randint(6, 10))


# login
print('Please manually complete the verification if necessary.')
login()
time.sleep(40)

# crawl the user files
crawl_user_files()
