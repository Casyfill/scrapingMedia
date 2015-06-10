#!/usr/bin/env python
#-*- coding: utf-8 -*-

# stem word using usning nltk.snowball algorythm
def stem(word):
	stemmed = word
	return stemmed

# text to stemmed_dictionary
def toDict(text, stop=[]):
	# transform text to dictionary of stemmed words usning nltk.snowball algorythm
	import re, nltk
	unstemmed = text.replace('\n','').split(' ')
	
	# general statistics
	words = len(unstemmed)

	# TODO: better sentence counter
	sentences = len([x for x in text.split('.') if len(x)>5]) # count all centences divided by '.'
	
	# TODO: stem
	stemmed = [stem(w) for w in unstemmed]

	d = {}
	for w in stemmed:
		if w in stop:
			pass
		else:
			d[w]=d.get(w,1)


	return d