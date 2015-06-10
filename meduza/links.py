#!/usr/bin/env python
## Philipp Kats (c) April 2015

## This script collects news links from news outlet meduza.ru
## Helping Andrew Simonov with his dissertation

import datetime, requests, scraperwiki, json,time
import lxml.html

baselink = 'https://meduza.io/api/v3/search'
types = ('news', 'cards', 'articles', 'shapito', 'polygon')

offset = 0
params = {'chrono':'articles', 'locale':'ru', 'per_page':100, 'page':offset}



unique_keys=['link']

while True:
    time.sleep(3)
    params['page']= params['page'] +1
    pResponse = json.loads(requests.get(baselink,params=params, verify=False).content )
    
    for link in pResponse['collection']:
        l = pResponse['documents'][link]
        
        title = l['title']
        date =  l['pub_date']
        dType = l['document_type']
        v = l['version']
        try:
            banners = l['with_banners']
        except:
            banners = None
        
        try:
            authors = ', '.join([x[0] for x in l['authors']])
        except:
            authors = None
        
        try:
            source = l['source']['url']
        except:
            source = None

        row = {'title':title, 'link':link, 'date':date,'dType':dType, 'v':v,'source':source, 'authors':authors,'banners':banners}
        print params['page'], title
        scraperwiki.sql.save(unique_keys, row)
        
    # if this is the last page of collection
    if pResponse['has_next']==False:
        break

