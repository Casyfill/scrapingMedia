#!/usr/bin/env python
## Philipp Kats (c) May 2015

## This script collects news links from news outlet GAZETA.ru
## Helping Andrew Simonov with his dissertation

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.PhantomJS(executable_path="/usr/local/bin/phantomjs",service_args=['--ssl-protocol=any'])
driver.set_window_size(1120, 550)
driver.get("http://top.rbc.ru/")

def click(driver):
	# clicks the upload button
	WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.LINK_TEXT, "Показать еще 12 новостей")))
	driver.find_element_by_link_text("Показать еще 12 новостей").click()
	# driver.implicitly_wait(2)


print
# print 'before:', len(driver.find_elements_by_css_selector('div.news-item-viewport__col-33p'))

for x in xrange(20):
	click(driver)
	lastOne = driver.find_elements_by_css_selector('div.news-item-viewport__col-33p')[-1]
	date = lastOne.find_element_by_css_selector('span.news-item-viewport__gray').text
	# print 'try%d' %x, len(driver.find_elements_by_css_selector('div.news-item-viewport__col-33p'))
	print 'try%d' %x, date

print "we've done here!"
driver.quit()