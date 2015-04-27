#!/usr/bin/env python
## Philipp Kats (c) April 2015

## This script collects news links from news outlet echo.msk.ru
## Helping Andrew Simonov with his dissertation

import datetime, requests, scraperwiki
import lxml.html

base = "http://echo.msk.ru/news/*.html?"

today = datetime.date.today()
startDate = datetime.date(2013, 04, 01) - datetime.timedelta(days=1) # to including first day

strForm = '%Y/%m/%d' # take a look here: https://docs.python.org/2/library/datetime.html#strftime-and-strptime-behavior
unique_keys = ['link'] #key attributes used to define unique rows (not to update them)


def datesArray(endDate,StartDate, strForm):
    # generate a string representation for each date between those two
    numdays = (endDate-StartDate).days
    return [(today - datetime.timedelta(days=x)).strftime(strForm) for x in range(0, numdays)]



def scrapeDate(date,base,unique_keys):
    # scraping link and 
    link = base.replace('*', date)
    html = requests.get(link)
    
    dom = lxml.html.fromstring(html.content)
    
    UL = dom.cssselect("body > div.pagecontent > div.main > div > section.content > div > div > div.rel > div > h3 > a")
    for li in UL:
        link = li.get("href").strip()
        if 'echo.' in link:
            # print date
            scraperwiki.sql.save(unique_keys, {'link':'http://echo.msk.ru'+link, 'date':date})
        else:
            print link

# print datesArray( today, startDate, strForm)
for date in datesArray( today, startDate, strForm):
    print date
    scrapeDate(date,base,unique_keys)
    
