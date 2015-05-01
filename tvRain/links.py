#!/usr/bin/env python
## Philipp Kats (c) April 2015

## This script collects news links from news outlet tvrain
## Helping Andrew Simonov with his dissertation

import datetime, requests, scraperwiki
import lxml.html

base = "http://tvrain.ru/archive/?search_year=%d&search_month=%d&search_day=%d&query="

today = datetime.date.today()
startDate = datetime.date(2013, 04, 01) - datetime.timedelta(days=1) # including first day

strForm = '%Y/%m/%d' # take a look here: https://docs.python.org/2/library/datetime.html#strftime-and-strptime-behavior
unique_keys = ['link','date'] #key attributes used to define unique rows (not to update them)


def datesArray(endDate,StartDate, strForm):
    # generate a string representation for each date between those two
    numdays = (endDate-StartDate).days
    return [(today - datetime.timedelta(days=x)) for x in range(0, numdays)]



def scrapeDate(date,base,unique_keys):
    strDate= date.strftime('%Y/%m/%d')
    # scraping link and additional data
    link = base % (date.year, date.month, date.day) # add date to link
    print 'baselink:', link
    html = requests.get(link) 
    dom = lxml.html.fromstring(html.content)
    # get total number of pages
    try:
        totalPages = int(dom.cssselect("#grid > div.col.c12.first > div > div > div > a")[-1].text)
    except:
        totalPages = 1
    # print totalPages
    
    for page in xrange(totalPages):
        pageLink = link + '&page=%d' %(page+1)
        print pageLink
        
        html = requests.get(pageLink) 
        dom = lxml.html.fromstring(html.content)
        
        articles = dom.cssselect("#grid > div.col.c12.first > div > div > section > div.clearfix > div.article-item")    
        # print len(articles)
        for article in articles:
            title = article.cssselect('a.article-item__title')[0].text.strip()
            newslink = 'http://tvrain.ru' +article.cssselect('a.article-item__title')[0].get('href')
            
            
            try:
                theme = article.cssselect(' a.article-item__subcategory')[0].text
            except: 
                theme = ''
            
            scraperwiki.sql.save(unique_keys, {'link':newslink, 'date':date,'theme':theme,'title':title})
            
        
    

# print datesArray( today, startDate, strForm)
for date in datesArray( today, startDate, strForm):
    # print date
    scrapeDate(date,base,unique_keys)
    
