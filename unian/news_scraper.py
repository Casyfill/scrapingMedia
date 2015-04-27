#!/usr/bin/env python
## Philipp Kats (c) April 2015

## This script collects news data archive from news outlet unian.net
## Helping Andrew Simonov with his dissertation

import requests, scraperwiki, json, urllib, time,random
import lxml.html


# samplelink = 'http://www.unian.net/politics/1068006-poyavilis-podrobnosti-ubiystva-buzinyi-strelyali-iz-pistoleta-tt-est-5-svideteley-foto.html'
# sapmlequery = 'select%20%0A%20%20%20%20link%0Afrom%20swdata%0AORDER%20BY%20date%20ASC%0ALIMIT%2015000%20%0AOFFSET%2015000%3B'

steak = 15000 #rows in one pass
# its=2 #passes done already (for offset purpose)
offset = 138995
q  =  urllib.quote('SELECT link FROM swdata ORDER BY date ASC LIMIT %d OFFSET %d' %(steak,offset))
l = requests.get('https://premium.scraperwiki.com/rekmggt/x20tbswbppg6yqd/sql/?q='+ q).json()
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
        
        title = dom.cssselect("#container > div.left_top > div.central_article > h1")[0].text
        topic = dom.cssselect("#container > div.left_top > div.breadcrumb > span > a")[0].text
        
        date = dom.cssselect('#container > div.left_top > div.central_article > div.date')[0].text.split('|')[0].strip()
        text = dom.cssselect('#container > div.left_top > div.central_article > div.article_body')[0].text_content().replace('\n', ' ').replace('\r', '').strip()
        fb, vk, tw, gp, odn = (x.text for x in dom.cssselect("#container > div.left_top > div.social_btns > a > span"))
        
        try:
            comments = int(dom.cssselect('#comments > div > h4')[0].text.split('-')[1].strip())
        except:
            comments = 0
    
        # print comments
        # print text
        unique_keys = ['link']
        scraperwiki.sql.save(unique_keys, {'link':link, 'date':date, 'topic':topic,'title':title,'text':text, 'fb':fb, 'tw':tw, 'vk':vk,'ggl':gp, 'odn':odn, 'comments':comments})

count = offset+1
for x in l:
    print count
    count+=1
    link = x['link']
    if 'http:' in link and 'unian.' in link  : #validating link
        try:
            scrapeLink(link)
            # time.sleep(random.randint(0, 3))
        except Exception,e: 
            try: print str(e)
            except: pass
        
            print 'someting wrong with the page:'
            print link
        
            
            
        
    else:
        print 'link is ivalid:' + link
