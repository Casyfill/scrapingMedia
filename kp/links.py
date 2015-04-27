#!/usr/bin/env python
## Philipp Kats (c) April 2015

## This script collects news links from news outlet kp.ru
## Helping Andrew Simonov with his dissertation

import datetime, requests, scraperwiki
import lxml.html

base = "http://www.kp.ru/online/archive/*"

today = datetime.date.today()
startDate = datetime.date(2013, 04, 01) - datetime.timedelta(days=1) # including first day

strForm = '%Y/%m/%d' # take a look here: https://docs.python.org/2/library/datetime.html#strftime-and-strptime-behavior
unique_keys = ['link','date'] #key attributes used to define unique rows (not to update them)


def datesArray(endDate,StartDate, strForm):
    # generate a string representation for each date between those two
    numdays = (endDate-StartDate).days
    return [(today - datetime.timedelta(days=x)).strftime(strForm) for x in range(0, numdays)]



def scrapeDate(date,base,unique_keys):
    # scraping link and additional data
    link = base.replace('*', date) # add date to link
    # print link
    html = requests.get(link) 
    dom = lxml.html.fromstring(html.content)
    
    themes = dom.cssselect("body > div.all_page-bg > div > div.all_page > div.n_content > div.n_leftcol-top > div.n_brief > h2")[1:] # all but the date
    ULs = dom.cssselect("body > div.all_page-bg > div > div.all_page > div.n_content > div.n_leftcol-top > div.n_brief > ul")
    
    for i, theme in enumerate(themes): 
        th = theme.text
        links = ULs[i].cssselect('li > h4 > a')
    
        for li in links:
            link = 'http://www.kp.ru' +li.get("href").strip()
            scraperwiki.sql.save(unique_keys, {'link':link, 'date':date,'theme':th})
            

# print datesArray( today, startDate, strForm)
for date in datesArray( today, startDate, strForm):
    print date
    scrapeDate(date,base,unique_keys)
    
