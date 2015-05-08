#!/usr/bin/env python
## Philipp Kats (c) May 2015

## This script collects news links from news outlet GAZETA.ru
## Helping Andrew Simonov with his dissertation
# scraped all after 19.02.2015
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

screenShotPath = "/Users/casy/Dropbox/My_Projects/ANDREW_media/scrapingMedia/regnum/screen.png"

#### SCRIPT START
print
print 'started'
driver = webdriver.PhantomJS(executable_path="/usr/local/bin/phantomjs",service_args=['--ssl-protocol=any'])
driver.set_window_size(1120, 550) # this is just work around the bug in selenium
driver.get("http://www.gazeta.ru/news/")

filepath = "/Users/casy/Dropbox/My_Projects/ANDREW_media/scrapingMedia/gazeta/links_try2.csv"
headersList=['date','theme','link']

# save_to_file
writeFile = open(filepath,'wb')
wD = csv.DictWriter(writeFile, headersList,restval='', extrasaction='raise', dialect='excel')
wD.writeheader()

	

harvest = 0 # input fasceting variable

while True:
	# click'n'save until the Date
	chunks = len(driver.find_elements_by_css_selector('div[id~=other_place]>article'))
	driver.find_element_by_link_text("Показать еще новости").click()
	
	WebDriverWait(driver, 4).until(len(driver.find_elements_by_css_selector('div[id~=other_place] > article'))>chunks)
	articles = driver.find_elements_by_css_selector('article.b-article')
	
	# subsetting input
	newHarvest = articles[harvest:len(articles)] #subset result to new ones only
	harvest = len(articles) #update harvest num


	for article in newHarvest:
		date = article.find_elements_by_css_selector('time')[0].text.split(',')[0]
		th = article.find_elements_by_css_selector('h2 > a')[0].text.encode('utf8','ignore')
		link = article.find_elements_by_css_selector('h2 > a')[0].get_attribute('href')
		print date,th,link
		wD.writerow({'date':date,'theme':th,'link':link})
	
	# isn't it the proper date to stop?
	lastDate = articles[-1].find_elements_by_css_selector('time')[0].text
	
	print lastDate
	if '30.03.2013' in lastDate: 
		print 'Hoorah!'
		break
	# now click that button
	
	

print "we've done here!"
driver.quit()