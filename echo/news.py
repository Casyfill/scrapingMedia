#!/usr/bin/env python
# -*- coding: utf-8 -*-
## Philipp Kats (c) April 2015

## This script collects news data archive from news outlet echoMSK
## Helping Andrew Simonov with his dissertation

import requests, scraperwiki, json, urllib, time,random
import lxml.html

months = {u'апреля':'04',u'мая':'05',u'июня':'06',u'июля':'07',u'августа':'08',u'сентября':'09',u'октября':'10',u'ноября':'11',u'декабря':'12',u'января':'01',u'февраля':'2',u'марта':'3'}
samplelink = 'http://echo.msk.ru/news/1253354-echo.html'
# sapmlequery = 'select%20%0A%20%20%20%20link%0Afrom%20swdata%0AORDER%20BY%20date%20ASC%0ALIMIT%2015000%20%0AOFFSET%2015000%3B'

steak = 10000 #rows in one pass

offset = 149473
q  =  urllib.quote('SELECT link FROM swdata ORDER BY date ASC LIMIT %d OFFSET %d' %(steak,offset))
l = requests.get('https://premium.scraperwiki.com/y0x87lt/6szw9xyxzyqlbid/sql/?q='+ q).json()
# print len(l)

def scrapeLink(link):
    # scraping link to MYSQL
    
    html = requests.get(link)
    
    if html.status_code != requests.codes.ok:
        print 'server goes bad'
        print html.status_code
        return
    else:
        
        dom = lxml.html.fromstring(html.content)
        
        title = dom.cssselect("body > div.pagecontent > div.main > div > section.content > div > div.conthead.news > h1")[0].text
        
        
        date = dom.cssselect('body > div.pagecontent > div.main > div > section.content > div > div.conthead.news > div.date > span')[0].text.strip()
        
        for k in months.keys():
            if k in date: date = date.replace(k,months[k])#.strip().replace(' ','.')
        
        
        text = dom.cssselect('body > div.pagecontent > div.main > div > section.content > div > div.typical > span')[0].text_content().replace('\n', ' ').replace('\r', '').strip()
        
        tw, fb, vk = (int(s.text.strip()) for s in dom.cssselect('#social_block > span.iblock > a > span'))
        
        
        
        comments = int(dom.cssselect('.actionBlock > div > a.comm > span.count')[0].text.strip())
        views = int(dom.cssselect(".actionBlock > div > a.view > span.count")[0].text.strip())
        # print comments, views 
    
        unique_keys = ['link']
        scraperwiki.sql.save(unique_keys, {'link':link, 'date':date, 'title':title,'text':text, 'fb':fb, 'tw':tw, 'vk':vk,'comments':comments,'views':views})

# scrapeLink(samplelink)
count = offset+1
for x in l:
    print count
    count+=1
    link = x['link']
    if 'http:' in link and 'echo.msk.' in link  : #validating link
        try:
            scrapeLink(link)
            # time.sleep(random.randint(0, 3))
        except Exception,e: 
            try: print str(e)
            except: pass
        
            print 'someting wrong with the page:'
            print link
        
            
            
        
    else:
        print 'link is invalid:' + link
