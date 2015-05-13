#!/usr/bin/env python
## Philipp Kats (c) April 2015

## This script collects news links from news outlet 1tv.ru
## Helping Andrew Simonov with his dissertation
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.PhantomJS(executable_path='/home/node_modules/phantomjs/bin/phantomjs')
driver.set_window_size(1120, 550) # this is just work around the bug in selenium

import datetime, requests, scraperwiki
import lxml.html

base = "http://www.1tv.ru/newsarchive/*"

# thisday = datetime.date.today()
thisday = datetime.date(2013, 9, 23)
startDate = datetime.date(2013, 04, 01) - datetime.timedelta(days=1) # including first day

strForm = '%d.%m.%Y' # take a look here: https://docs.python.org/2/library/datetime.html#strftime-and-strptime-behavior
unique_keys = ['link'] #key attributes used to define unique rows (not to update them)


def datesArray(endDate,StartDate, strForm):
    # generate a string representation for each date between those two
    numdays = (endDate-StartDate).days
    return [(endDate - datetime.timedelta(days=x)).strftime(strForm) for x in range(0, numdays)]



def scrapeDate(date,base,unique_keys):
    # scraping link and additional data
    link = base.replace('*', date) # add date to link
    # print link
    # print link
    driver.get(link)
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "n_list-news")))
    articles = element.find_elements_by_css_selector('#list_news_search > div.n_list-news > ul > li > div.txt > p')
    # print len(articles)
    for article in articles:
        link = 'http://www.1tv.ru' +article.find_elements_by_css_selector('p>a')[0].get_attribute("href")
        title = article.find_elements_by_css_selector('p>a')[0].text
        # print link, title, date
        scraperwiki.sql.save(unique_keys, {'link':link, 'date':date,'theme':title})
            

# print datesArray( today, startDate, strForm)

for date in datesArray( thisday, startDate, strForm):
    print date
    scrapeDate(date,base,unique_keys)
    
