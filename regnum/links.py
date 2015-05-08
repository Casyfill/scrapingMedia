#!/usr/bin/env python
## Philipp Kats (c) April 2015

## This script collects news links from news outlet regnum.ru
## Helping Andrew Simonov with his dissertation

import datetime, requests, scraperwiki
import lxml.html

base = "http://regnum.ru/hotnews/?page*"
unique_keys = ['link'] #key attributes used to define unique rows (not to update them)
endPage = 229 +1


def scrapeDate(pageNum,base,unique_keys,count):
    # scraping link and additional data
    link = base.replace('*', str(pageNum)) # add date to link
    # print link
    html = requests.get(link) 
    dom = lxml.html.fromstring(html.content)
    

    articles = dom.cssselect("#col1 > ul.topnewsroll > li")
    
    for a in articles:
        th = a.cssselect('a')[0].text.strip()
        link = 'http://regnum.ru' + a.cssselect('a')[0].get("href")
        scraperwiki.sql.save(unique_keys, {'link':link, 'date':'na','theme':th})
        count+=1
        print count
    
    return count
        
            

# print datesArray( today, startDate, strForm)
count=0
for x in xrange(1,endPage):
    # print x
    count = scrapeDate(x,base,unique_keys,count)
    
