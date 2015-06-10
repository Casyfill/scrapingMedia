#-*- coding: utf-8 -*-
# import sys
import os
from nltk.stem import SnowballStemmer
import re

stemmer = SnowballStemmer("russian")

# Определяем имя файлв
def name(s):
	n = s.split('/')[-1].split('.')[0] + '.csv'
	return n
	pass

# Создаем словарик
def generateFDict(filename):
	import chardet
	import codecs

	# РАСПОЗНАЕМ КОДИРОВКУ
	bytes = min(32, os.path.getsize(filename))
	raw = open(filename, 'rb').read(bytes)

	if raw.startswith(codecs.BOM_UTF8):
	    encoding = 'utf-8-sig'
	else:
	    result = chardet.detect(raw)
	    encoding = result['encoding']

	infile = codecs.open(filename, 'r', encoding=encoding)
	txt = infile.read()
	infile.close()

	# ПЕРЕВОДИМ В ЮНИКОД
	text = unicode(txt)

	# СОСТАВЛЯЕМ СЛОВАРЬ РЕГУЛЯРОЧКОЙ
	hello_pattern = re.compile( u'([А-Яа-я]+)', re.UNICODE )
	Wlist = hello_pattern.findall( text )

	print filename.split('/')[-1].split('.')[0], ':', len(Wlist)
	# ПЕЧАТАЕМ
	# for l in Wlist:
	# 	word = unicode(l).lower()
	# 	print word,'|',stemmer.stem(word)

	# СТЕММИМ И СОСТАВЛЯЕМ СЛОВАРИК
	Text_Dict = {}

	for w in Wlist:
		word = unicode(w).lower()
		wStemmed = stemmer.stem(word)
		if wStemmed not in Text_Dict.keys():
			Text_Dict[wStemmed]={}
			Text_Dict[wStemmed]['dict'] = []
			Text_Dict[wStemmed]['dict'].append(word)
			Text_Dict[wStemmed]['count'] = 1
		else:
			Text_Dict[wStemmed]['dict'].append(word)
			Text_Dict[wStemmed]['count'] += 1


	# РАЧИТЫВАЕМ И ПЕЧАТАЕМ СТАТИСТИУ

	resList = []
	for key in Text_Dict.keys():
		# print key , ':', (', ').join(Text_Dict[key])
		rString =  key + '|' + str(Text_Dict[key]['count'])  + '|' + (',').join(Text_Dict[key]['dict'])
		# print rString
		rString= rString + '\n'
		resList.append(rString.encode('utf-8'))

	resList[-1].replace('\n','')
	return resList
	pass


# создаем список файлов в папке

fileList = []
basePath = "/Users/andy/Dropbox/Projects/Kats/RIA/2013_11_28_President_speech/texts/"
os.chdir(basePath)
for files in os.listdir("."):
	if files[-3:] =='txt':
		filename = basePath + files
		# print 'файл: ', files
		fileList.append(filename)

for files in fileList:
	# для каждого файлв узнаем имя и создае словарь
	n = name(files)

	result = generateFDict(files)

	#  для каждого файла сохраняем словарик
	workfile ='/Users/andy/Dropbox/Projects/Kats/RIA/2013_11_28_President_speech/Dicts/' + n

	f = open(workfile, 'w')
	write_data = f.writelines(result)
	f.closed
	# print n, ' done'

print 'all functions are done'