#!/usr/bin/env python
# -*- coding: utf-8 -*-
## Philipp Kats (c) April 2015

## This script collects news data archive from news outlet TV RAIN
## Helping Andrew Simonov with his dissertation

import requests, scraperwiki, json, urllib, time,random
import lxml.html

# months = {u'апреля':'04',u'мая':'05',u'июня':'06',u'июля':'07',u'августа':'08',u'сентября':'09',u'октября':'10',u'ноября':'11',u'декабря':'12',u'января':'01',u'февраля':'2',u'марта':'3'}
# samplelink = 'http://tvrain.ru/teleshow/novosti_sajta/kapitanom_sbornoj_rossii_po_figurnomu_kataniju_v_sochi_budet_ekaterina_bobrova-362118/'
# sapmlequery = 'select%20%0A%20%20%20%20link%0Afrom%20swdata%0AORDER%20BY%20date%20ASC%0ALIMIT%2015000%20%0AOFFSET%2015000%3B'

steak = 10000 #rows in one pass

offset = 44770
q  =  urllib.quote('SELECT link FROM swdata ORDER BY date ASC LIMIT %d OFFSET %d' %(steak,offset))
l = requests.get('https://premium.scraperwiki.com/yjw43kk/cla2j95pmunpd60/sql/?q='+ q).json()

print len(l)

def scrapeLink(link):
    # scraping link to MYSQL
    
    html = requests.get(link)
    
    if html.status_code != requests.codes.ok:
        print 'server goes bad'
        print html.status_code
        return
    else:
        
        dom = lxml.html.fromstring(html.content)
        
        # title and date
        title = dom.cssselect("h1")[0].text
        date = dom.cssselect('time')[0].get('datetime').split(' ')[0]
        
        # text
        try:
            text = dom.cssselect('div.summary')[0].text_content().replace('\n', ' ').replace('\r', '').strip()
        except:
            text = ''
        try:
            text2 = dom.cssselect('div.article-full__text')[0].text_content().replace('\n', ' ').replace('\r', '').strip()
            text +=text2 
        except:
            pass
        
        try: 
            text3 = dom.cssselect("#grid > div.col.c12.first > div > article > div.content")[0].text.replace('\n', ' ').replace('\r', '').strip()
            text+=text3
        except:
            pass
        
        
        
        # social networks
        fb, tw, gp, vk = 0,0,0,0 #now this dont work
        comments, views = -1,-1
        # comments, views, tags
        if len(dom.cssselect('#grid > div.col.c12.first > div > div.col.c8.first.alpha > article > div > div.meta.baseline-wrapper'))!=0:
            ctype= 'text'
            views = int(dom.cssselect("div.meta.baseline-wrapper > span > span")[0].text.replace(' ',''))
            comments = int(dom.cssselect("div.meta.baseline-wrapper > a > span")[0].text.replace(' ',''))
            # print ctype, views, comments
            
        elif len(dom.cssselect('#grid > div.col.c12.first > div.alpha.alpha_has_access > article > ul'))!=0:
            ctype= 'video/image'
            views = int(dom.cssselect("div.alpha.alpha_has_access > article > ul > li:nth-child(3) > span:nth-child(2)")[0].text.replace(' ',''))
            comments = int(dom.cssselect("div.alpha.alpha_has_access > article > ul > li:nth-child(4) > a > span:nth-child(2)")[0].text.replace(' ',''))
            # print ctype, views, comments
        
        elif len(dom.cssselect('article > div.meta.baseline-wrapper > span:nth-child(2) > span'))!=0:
            ctype ='spc'
            
            views = int(dom.cssselect("#grid > div.col.c12.first > div > article > div.meta.baseline-wrapper > span:nth-child(2) > span")[0].text.replace(' ',''))
            comments = int(dom.cssselect("#grid > div.col.c12.first > div > article > div.meta.baseline-wrapper > span:nth-child(3) > a > span")[0].text.replace(' ',''))
            # print ctype, views, comments
        elif len(dom.cssselect("article > div.content > div.baseline-wrapper > ul > li:nth-child(2) > span"))!=0:
            ctype = 'photo'
            views = int(dom.cssselect("article > div.content > div.baseline-wrapper > ul > li:nth-child(2) > span")[0].text.replace(' ',''))
            comments = 0
            # print ctype, views, comments
        elif len(dom.cssselect('article > ul:nth-child(3) > li:nth-child(2) > span:nth-child(2)'))!=0:
            ctype = 'blog'
            views = int(dom.cssselect("article > ul:nth-child(3) > li:nth-child(2) > span:nth-child(2)")[0].text.replace(' ',''))
            comments = int(dom.cssselect("article > ul:nth-child(3) > li:nth-child(3) > a > span:nth-child(2)")[0].text.replace(' ',''))
        elif len(dom.cssselect('article > ul.meta > li span:nth-child(2)'))!=0:
            ctype = 'closedShow'
            views = int(dom.cssselect("article > ul > li:nth-child(3) > span:nth-child(2)")[0].text.replace(' ',''))
            comments = int(dom.cssselect("article > ul > li:nth-child(4) > a > span:nth-child(2)")[0].text.replace(' ',''))
        elif len(dom.cssselect("article > div > div.meta.baseline-wrapper > span > span"))!=0:
            ctype = 'tweet'
            views=int(dom.cssselect("article > div > div.meta.baseline-wrapper > span > span")[0].text.replace(' ',''))
            comments=int(dom.cssselect("article > div > div.meta.baseline-wrapper > a > span")[0].text.replace(' ',''))
        elif len(dom.cssselect("article > div.baseline-wrapper > span > span > span"))!=0:
            ctype = 'tvshow'
            views=int(dom.cssselect("article > div.baseline-wrapper > span > span > span")[0].text.replace(' ',''))
            comments=int(dom.cssselect("article > div.baseline-wrapper > span > a > span")[0].text.replace(' ',''))
            
        else:
            ctype = '?'
            print '!!!!!!! problem parsing comments/views:', link
        
        tags = '|'.join([x.text for x in dom.cssselect("div.article-full-tags > div:nth-child(1) > div.article-full-tags__tags > a")])
        # print views, comments, tags
        
            
        unique_keys = ['link']
        scraperwiki.sql.save(unique_keys, {'link':link, 'date':date, 'title':title,'text':text, 'fb':fb, 'tw':tw, 'vk':vk, 'gp':gp,'comments':comments,'views':views,'tags':tags,'ctype':ctype})

# scrapeLink(samplelink) # testing

count = offset+1  #conveier
for x in l:
    print count
    count+=1
    link = x['link']
    if 'http:' in link and 'tvrain.ru' in link  : #validating link
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
