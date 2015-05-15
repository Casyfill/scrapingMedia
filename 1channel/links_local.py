#!/usr/bin/env python
## Philipp Kats (c) April 2015

## This script collects news links from news outlet 1tv.ru
## Helping Andrew Simonov with his dissertation
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.PhantomJS(executable_path="/usr/local/bin/phantomjs",service_args=['--ssl-protocol=any'])
driver.set_window_size(1120, 550) # this is just work around the bug in selenium
driver.implicitly_wait(2)

import datetime, requests, csv
import lxml.html
from time import sleep
base = "http://www.1tv.ru/newsarchive/*"
filepath = '/Users/casy/Dropbox/My_Projects/ANDREW_media/scrapingMedia/1channel/links2.csv'
screenShotPath = "/Users/casy/Dropbox/My_Projects/ANDREW_media/scrapingMedia/1channel/screen.png"
# thisday = datetime.date.today()
thisday = datetime.date(2013, 6, 17)
startDate = datetime.date(2013, 04, 01) - datetime.timedelta(days=1) # including first day

strForm = '%d.%m.%Y' # take a look here: https://docs.python.org/2/library/datetime.html#strftime-and-strptime-behavior
unique_keys = ['link'] #key attributes used to define unique rows (not to update them)


def datesArray(endDate,StartDate, strForm):
    # generate a string representation for each date between those two
    numdays = (endDate-StartDate).days
    return [(endDate - datetime.timedelta(days=x)).strftime(strForm) for x in range(0, numdays)]



def scrapeDate(date,base,unique_keys, wD):
    # scraping link and additional data
    link = base.replace('*', date) # add date to link
    # print link
    driver.get(link)
    try:
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "n_list-news")))
        articles = element.find_elements_by_css_selector('#list_news_search > div.n_list-news > ul > li > div.txt > p')
        print len(articles)
        for article in articles:
            link = 'http://www.1tv.ru' +article.find_elements_by_css_selector('p>a')[0].get_attribute("href")
            title = article.find_elements_by_css_selector('p>a')[0].text.encode('utf8','ignore')
            # print link, title, date
            wD.writerow({'link':link, 'date':date,'theme':title})
    except Exception, e:
        print str(e)
        driver.get_screenshot_as_file(screenShotPath)
                

# print datesArray( today, startDate, strForm)
headersList=['link','date','theme']

with open(filepath,'wb') as writeFile:
    wD = csv.DictWriter(writeFile, headersList,restval='', extrasaction='raise', dialect='excel')
    wD.writeheader()    
    for date in datesArray( thisday, startDate, strForm):
        print date
        scrapeDate(date,base,unique_keys, wD)
    
