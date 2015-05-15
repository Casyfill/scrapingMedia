#!/usr/bin/env python
# -*- coding: utf-8 -*-
## Philipp Kats (c) April 2015

## This script collects news data archive from news outlet channel1
## Helping Andrew Simonov with his dissertation

import requests, scraperwiki, json, urllib, time,random
import lxml.html


months = {u'апреля':'04',u'мая':'05',u'июня':'06',u'июля':'07',u'августа':'08',u'сентября':'09',u'октября':'10',u'ноября':'11',u'декабря':'12',u'января':'01',u'февраля':'2',u'марта':'3'}
# samplelink = 'http://www.kp.ru/online/news/1404729/'
# sapmlequery = 'select%20%0A%20%20%20%20link%0Afrom%20swdata%0AORDER%20BY%20date%20ASC%0ALIMIT%2015000%20%0AOFFSET%2015000%3B'

steak = 10000 #rows in one pass

offset = 18841
q  =  urllib.quote('SELECT link FROM swdata ORDER BY rdate ASC LIMIT %d OFFSET %d' %(steak,offset))
l = requests.get('https://premium.scraperwiki.com/y6ed9kx/vikyrscexgw3ypd/sql/?q='+ q).json()
# print l
# print len(l)

def scrapeLink(link):
    # scraping link to MYSQL
    link = link[17:].replace('http/','http:/')
    # print link
    html = requests.get(link)
    
    if html.status_code != requests.codes.ok:
        print 'server goes bad'
        print html.status_code
        return
    else:
        
        dom = lxml.html.fromstring(html.content)
        
        theme = link.split('/')[-2]
        
        title = dom.cssselect("#article_copy > h1")[0].text
        date = dom.cssselect('body > div.all_page > div.n_root > div.n_leftcol > div.title_ins > h4 > span')[0].text.strip().split(',')[0].lower()
        
        
        for k in months.keys():
            if k in date: date = date.replace(k,months[k]).strip().replace('  ',' ').replace(' ','.')
        # print date
        
        text = dom.cssselect('#article_copy')[0].text_content().replace('\n', ' ').replace('\r', '').strip()
        
        
        fb, tw, odn, vk = 0,0,0,0 #now this dont work

        tags = ','.join([x.text for x in dom.cssselect('#article_copy > div.tags >a')])
        # views = int(dom.cssselect(".actionBlock > div > a.view > span.count")[0].text.strip())
        # print comments, views 
    
        unique_keys = ['link']
        scraperwiki.sql.save(unique_keys, {'link':link, 'theme':theme, 'date':date, 'title':title,'text':text, 'fb':fb, 'tw':tw, 'vk':vk, 'odn':odn,'tags':tags})

# scrapeLink(samplelink)
count = offset+1
for x in l:
    print count
    count+=1
    link = x['link']
    if 'http:' in link and '1tv.ru' in link  : #validating link
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
