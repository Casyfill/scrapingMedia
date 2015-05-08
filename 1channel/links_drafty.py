#!/usr/bin/env python
## Philipp Kats (c) April 2015

## This script collects news links from news outlet kp.ru
## Helping Andrew Simonov with his dissertation
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.PhantomJS()

driver.set_window_size(1120, 550) # this is just work around the bug in selenium
driver.get("http://www.gazeta.ru/news/")

import datetime, requests, scraperwiki
import lxml.html

base = "http://www.1tv.ru/newsarchive/*"

today = datetime.date.today()
startDate = datetime.date(2013, 04, 01) - datetime.timedelta(days=1) # including first day

strForm = '%d.%m.%Y' # take a look here: https://docs.python.org/2/library/datetime.html#strftime-and-strptime-behavior
unique_keys = ['link'] #key attributes used to define unique rows (not to update them)


def datesArray(endDate,StartDate, strForm):
    # generate a string representation for each date between those two
    numdays = (endDate-StartDate).days
    return [(today - datetime.timedelta(days=x)).strftime(strForm) for x in range(0, numdays)]



def scrapeDate(date,base,unique_keys):
    # scraping link and additional data
    link = base.replace('*', date) # add date to link
    print link
    # print link
    html = requests.get(link) 
    dom = lxml.html.fromstring(html.content)
    
    
    articles = dom.cssselect("#list_news_search > div.n_list-news > ul > li:nth-child(1) > div.txt > p")
    print len(articles)
    for article in articles:
        link = 'http://www.1tv.ru' +article.cssselect('p>a')[0].get("href")
        title = article.cssselect('p>a')[0].text
        print link, title, date
        # scraperwiki.sql.save(unique_keys, {'link':link, 'date':date,'theme':title})
            

# print datesArray( today, startDate, strForm)
for date in datesArray( today, startDate, strForm):
    print date
    scrapeDate(date,base,unique_keys)
    
