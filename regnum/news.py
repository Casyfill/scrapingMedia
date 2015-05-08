#!/usr/bin/env python
# -*- coding: utf-8 -*-
## Philipp Kats (c) April 2015

## This script collects news data archive from news outlet Komsomolskaya Pravda
## Helping Andrew Simonov with his dissertation

import requests, scraperwiki, json, urllib, time,random
import lxml.html

months = {u'апреля':'04',u'мая':'05',u'июня':'06',u'июля':'07',u'августа':'08',u'сентября':'09',u'октября':'10',u'ноября':'11',u'декабря':'12',u'января':'01',u'февраля':'2',u'марта':'3'}
samplelink = 'http://regnum.ru/news/1739815.html'
# sapmlequery = 'select%20%0A%20%20%20%20link%0Afrom%20swdata%0AORDER%20BY%20date%20ASC%0ALIMIT%2015000%20%0AOFFSET%2015000%3B'

steak = 10000 #rows in one pass

offset = 10000
q  =  urllib.quote('SELECT link FROM swdata ORDER BY date ASC LIMIT %d OFFSET %d' %(steak,offset))
l = requests.get('https://premium.scraperwiki.com/dfjmgep/ngrkiccenuo5qcg/sql/?q='+ q).json()
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
        
        theme = dom.cssselect("#col1 > div.linenavigation > a ")[-2].text.strip()
        
        title = dom.cssselect("#col1 > div.newsbody > h1")[0].text
        date = dom.cssselect('#col1 > div.newsbody > div.date')[0].text.split(' ')[0]
        
    
        text = '\n'.join([x.text_content().replace('\n', ' ').replace('\r', '') for x in dom.cssselect('#col1 > div.newsbody > p')])
        
        
        fb, tw, odn, gp, vk, = 0,0,0,0,0 #now this dont work
    
        unique_keys = ['link']
        scraperwiki.sql.save(unique_keys, {'link':link, 'theme':theme, 'date':date, 'title':title,'text':text, 'fb':fb, 'tw':tw, 'vk':vk, 'gp':gp,'odn':odn})

# scrapeLink(samplelink)
count = offset+1
for x in l:
    print count
    count+=1
    link = x['link'].strip()
    if 'http:' in link and 'regnum.ru' in link  : #validating link
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
