#!/usr/bin/env python
#-*- coding: utf-8 -*-
import csv

filename1='/Users/casy/Dropbox/My_Projects/ANDREW_media/scrapingMedia/1channel/links.csv'
filename2='/Users/casy/Dropbox/My_Projects/ANDREW_media/scrapingMedia/1channel/links2.csv'
resultpath ='/Users/casy/Dropbox/My_Projects/ANDREW_media/scrapingMedia/1channel/links_all.csv' 

wD1, wD2 = [], []
with open(filename1,'rb') as readFile:
	wD1 = list(csv.DictReader(readFile, fieldnames=None, restkey=None, restval=None, dialect='excel'))

with open(filename2,'rb') as readFile:
	wD2 = list(csv.DictReader(readFile, fieldnames=None, restkey=None, restval=None, dialect='excel'))
	
rows = wD1 + wD2
print len(rows)
headersList=rows[0].keys()

with open(resultpath,'wb') as writeFile:
	wD = csv.DictWriter(writeFile, headersList,restval='', extrasaction='raise', dialect='excel')
	wD.writeheader()

	for row in rows:
		wD.writerow(row)

	print 'done!'