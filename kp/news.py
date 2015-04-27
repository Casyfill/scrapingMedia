#!/usr/bin/env python
# -*- coding: utf-8 -*-
## Philipp Kats (c) April 2015

## This script collects news data archive from news outlet Komsomolskaya Pravda
## Helping Andrew Simonov with his dissertation

import requests, scraperwiki, json, urllib, time,random
import lxml.html

months = {u'апреля':'04',u'мая':'05',u'июня':'06',u'июля':'07',u'августа':'08',u'сентября':'09',u'октября':'10',u'ноября':'11',u'декабря':'12',u'января':'01',u'февраля':'2',u'марта':'3'}
# samplelink = 'http://www.kp.ru/online/news/1404729/'
# sapmlequery = 'select%20%0A%20%20%20%20link%0Afrom%20swdata%0AORDER%20BY%20date%20ASC%0ALIMIT%2015000%20%0AOFFSET%2015000%3B'

steak = 10000 #rows in one pass

offset = 2768
q  =  urllib.quote('SELECT link FROM swdata ORDER BY date ASC LIMIT %d OFFSET %d' %(steak,offset))
l = requests.get('https://premium.scraperwiki.com/3ux35rt/tskxjfilolyryxx/sql/?q='+ q).json()
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
        
        theme = dom.cssselect("body > div.all_page-bg > div > div.article_page > div > div.a_leftcol > div.mistakes-editable > div.a_info > a")[0].text.strip()
        
                               
        title = dom.cssselect("body > div.all_page-bg > div > div.article_page > div > div.a_leftcol > div.mistakes-editable  h1")[0].text
        # print title
        date = dom.cssselect('body > div.all_page-bg > div > div.article_page > div > div.a_leftcol > div.mistakes-editable > div.a_info > div > a > span.left')[0].text.strip().split(',')[0].replace('(','').lower()
        
        for k in months.keys():
            if k in date: date = date.replace(k,months[k]).strip().replace(' ','.')
        # print date
        
        text1 = dom.cssselect('body > div.all_page-bg > div > div.article_page > div > div.a_leftcol > div.mistakes-editable > div.a_about')[0].text_content().replace('\n', ' ').replace('\r', '').strip()
        text2 = dom.cssselect('body > div.all_page-bg > div > div.article_page > div > div.a_leftcol > div.mistakes-editable > div.a_content')[0].text_content().replace('\n', ' ').replace('\r', '').strip()
        text = ' '.join([text1, text2])
        
        # sns = dom.cssselect('div.b-share_theme_counter > span > span.btn__wrap')
        # print len(sns)
        # tw, fb, vk = (int(s.text.strip()) for s in dom.cssselect('#social_block > span.iblock > a > span'))
        fb, tw, odn, gp, vk, ml = 0,0,0,0,0,0 #now this dont work

        comments = int(dom.cssselect('#cm-count-bottom > span')[0].text.strip())
        # views = int(dom.cssselect(".actionBlock > div > a.view > span.count")[0].text.strip())
        # print comments, views 
    
        unique_keys = ['link']
        scraperwiki.sql.save(unique_keys, {'link':link, 'theme':theme, 'date':date, 'title':title,'text':text, 'fb':fb, 'tw':tw, 'vk':vk, 'ml':ml, 'gp':gp,'odn':odn,'comments':comments,})

# scrapeLink(samplelink)
count = offset+1
for x in l:
    print count
    count+=1
    link = x['link']
    if 'http:' in link and 'kp.ru' in link  : #validating link
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
