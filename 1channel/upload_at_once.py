#!/usr/bin/env python
# -*- coding: utf-8 -*-
import scraperwiki, csv
import requests, urllib2


url = "https://dl.dropboxusercontent.com/u/9561169/links_all.csv"
unique_keys=['link']

# def utf_8_encoder(unicode_csv_data):
#     for line in unicode_csv_data:
#         yield unicode(line, 'utf-8')
        
responce = urllib2.urlopen(url)
wD = csv.DictReader(responce, fieldnames=None, restkey=None, restval=None, dialect='excel')
	
for row in wD:
    row['theme'] = row['theme'].decode('utf8','ignore')
    scraperwiki.sql.save(unique_keys, row)
    print row['theme']
# reader = csv.reader(html.content, delimiter=',', )
# print reader
# for row in reader:
#         print row

# Saving data:
# unique_keys = [ 'id' ]
# data = { 'id':12, 'name':'violet', 'age':7 }
# scraperwiki.sql.save(unique_keys, data)
