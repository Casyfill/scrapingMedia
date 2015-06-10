#!/usr/bin/env python
#-*- coding: utf-8 -*-
## Philipp Kats (c) May 2015

## This script collects news links from news outlet ria.ru
## Helping Andrew Simonov with his dissertation

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.PhantomJS(executable_path="/usr/local/bin/phantomjs",service_args=['--ssl-protocol=any'])
driver.set_window_size(1120, 550) # this is just work around the bug in selenium
# driver.implicitly_wait(5)

import datetime, requests, csv
import lxml.html
# from time import sleep

base = "http://ria.ru/archive/*/"
filepath = '/Users/casy/Dropbox/My_Projects/ANDREW_media/scrapingMedia/1channel/links2.csv'
screenShotPath = "/Users/casy/Dropbox/My_Projects/ANDREW_media/scrapingMedia/Ria/screen.png"
# thisday = datetime.date.today()
thisday = datetime.date(2013, 6, 17)
startDate = datetime.date(2013, 04, 01) - datetime.timedelta(days=1) # including first day

strForm = '%Y%m%d' # take a look here: https://docs.python.org/2/library/datetime.html#strftime-and-strptime-behavior
unique_keys = ['link'] #key attributes used to define unique rows (not to update them)


def datesArray(endDate,StartDate, strForm):
    # generate a string representation for each date between those two
    numdays = (endDate-StartDate).days
    return [(endDate - datetime.timedelta(days=x)).strftime(strForm) for x in range(0, numdays)]



def scrapeDate(date,base,unique_keys):
    # scraping link and additional data
    link = base.replace('*', date) # add date to link
    # print link
    driver.get(link)

    # input fasceting variable
    try:
        clickclick(driver)
    except Exception,e:
        print str(e)
        driver.get_screenshot_as_file(screenShotPath)

def clickclick(driver):
    lists = 1 
    while driver.find_element_by_class_name("list_pagination_next")!=None :
        # print EC.presence_of_element_located((By.CLASS_NAME, "list_pagination_next"))
        driver.find_element_by_class_name("list_pagination_next").click()# click all the way for the Date
        WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.list:nth-child(%d)" %(lists+1))))
        lists+=1
        articles = driver.find_elements_by_css_selector('div.rubric_container div.list_item')
        print len(articles)
    return articles
    

         
print 'started'
scrapeDate('20150507',base,unique_keys)
# print datesArray( today, startDate, strForm)
# headersList=['link','date','theme']

# with open(filepath,'wb') as writeFile:
#     wD = csv.DictWriter(writeFile, headersList,restval='', extrasaction='raise', dialect='excel')
#     wD.writeheader()    
#     for date in datesArray( thisday, startDate, strForm):
#         print date
#         scrapeDate(date,base,unique_keys, wD)
    
