#!/usr/bin/env python
# -*- coding: utf-8 -*-
## Philipp Kats (c) June 2015

## This script collects news data archive from news outlet Meduza.io
## Helping Andrew Simonov with his dissertation

import requests, scraperwiki, json, urllib, time,random
import lxml.html

steak = 10000 #rows in one pass

offset = 6743
q  =  urllib.quote('SELECT link FROM swdata ORDER BY date ASC LIMIT %d OFFSET %d' %(steak,offset))
l = requests.get('https://premium.scraperwiki.com/moyxvyl/xfbdf0pbjygr3ye/sql/?q='+ q).json()

def scrapeLink(link):
    # scraping link to MYSQL
    
    html = requests.get(link, verify=False)
    
    if html.status_code != requests.codes.ok:
        print 'server goes bad'
        print html.status_code
        return
    else:
        dom = lxml.html.fromstring(html.content)
        title = dom.cssselect('div.NewsTitle')[0].text_content().replace('\n', ' ').replace('\r', '').strip()
        text = dom.cssselect('div.DangerousHTML')[0].text_content().replace('\n', ' ').replace('\r', '').strip()
        
        
        # print title
        fb, tw, vk = 0,0,0 #now this dont work
        unique_keys = ['link']
        scraperwiki.sql.save(unique_keys, {'link':link, 'title':title,'text':text, 'fb':fb, 'tw':tw, 'vk':vk})


# scrapeLink('https://meduza.io/news/2014/10/13/v-radu-vnesli-zakonoproekt-o-vyhode-iz-sng')
count = offset+1
for x in l:
    print count
    count+=1
    link = 'https://meduza.io/'+ x['link']
    if 'meduza.io' in link  : #validating link
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
