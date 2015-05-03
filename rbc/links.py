#!/usr/bin/env python
#-*- coding: utf-8 -*-

from selenium import webdriver

# browser = webdriver.PhantomJS(executable_path="/usr/local/bin/phantomjs")
# browser.get("http://openbsd.org/")

from selenium import webdriver
driver = webdriver.PhantomJS(executable_path="/usr/local/bin/phantomjs")
driver.set_window_size(1120, 550)
driver.get("https://duckduckgo.com/")
print driver.page_source()
# driver.find_element_by_id('search_form_input_homepage').send_keys("realpython")
# driver.find_element_by_id("search_button_homepage").click()
browser.page_source.
driver.quit()