#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division
import os, sys, string, re, codecs

#path = os.path.dirname(os.path.abspath(__file__)) if __file__ else os.getcwd()
path = os.getcwd() #get current working directory
reMarks = re.compile("[.,:;!?()/<>«»'\"]")
reLineBreaks = re.compile("[\r\n]")
reSpaces = re.compile("[ ][ ]+")
reText=re.compile("(\.txt|\.pdf)$")
dictionary={}
#PyPDF2
#sys.exit()

def clean_text(text):
	text = reMarks.sub(' ', text)
	text = reSpaces.sub(' ', text)
	text = reLineBreaks.sub('', text)
	text = text.lower()
	text = text.strip()
	return text

def read_text(fileName):
	f = codecs.open(fileName, 'r', 'utf-8-sig')
	lines = f.readlines()
	f.close()
	return lines

def write_csv(counts, keywordTotalCount, keywordCount, wordCount, fileName):
	parts = fileName.split('/')
	f = codecs.open(path + '/count.csv', 'a', 'utf-8-sig')
	for count in counts:
		f.write(fileName + ',' + parts[1] + ',' + parts[2] + ',' + parts[3] + ',' + parts[4].split('_')[0] + ',' + count[0] + ',' + str(count[1])+ ',' + str(keywordTotalCount) + ',' + str(round(keywordTotalCount/keywordCount, 2)) + ',' + str((keywordTotalCount/wordCount)*1000)+ ',' + str(wordCount) + '\n')
	f.close()

def write_kwic_csv(counts, kwics, fileName):
	parts = fileName.split('/')
	f = codecs.open(path + '/kwic.csv', 'a', 'utf-8-sig')
	for count in counts:
		for kwic in kwics[count[0]]:
			f.write(fileName + ',' + parts[1] + ',' + parts[2] + ',' + parts[3] + ',' + parts[4].split('_')[0] + ',' + count[0] + ',' + str(count[1])+ ',"' + kwic + '"\n')
	f.close()
	
def read_dictionary():
	f = codecs.open(path + '/dictionary.txt', 'r', 'utf-8-sig')
	lines = f.readlines()
	f.close()
	for line in lines:
		if line[0] != '#' and len(line.strip()):
			line = line.replace(';', ',')
			label = line.strip().split(':')[0].split(',')
			words = line.strip().split(':')[1].split(',')
			dictionary[label[2]] = words
					
def text_count(fileName, keywords):
	lines = read_text(fileName)
	counts = {}
	wordCount = 0
	for line in lines:
		words = clean_text(line).split(' ')
		wordCount += len(words)
		for word in words:
			if len(word) > 0:
				if counts.has_key(word):
					counts[word] += 1
				else:
					counts[word] = 1
	return [counts, wordCount]

def kwic(fileName, keywords):
	print fileName
	kwics = {}
	lines = read_text(fileName)
	for line in lines:
		for keyword in keywords: kwics[keyword]=[]
		words = clean_text(line).split(' ')
		for keyword in keywords:
			for i, word in enumerate(words):
				print word
				print keyword
				if word == keyword:
					if (i-10)<0:
						start=0
					else:
						start=i-10
					if (i+10)>len(words)-1:
						end=len(words)-1
					else:
						end=i+10
					kwics[keyword].append(' '.join(words[start: end]))
					
	#for w in keywords:   
	    #print w
	    #print kwics[w]
	return kwics

def find_keywords(keywords, fileName):
	counts, wordCount = text_count(fileName, keywords)
	keywordCounts = []
	keywordTotalCount = 0
	keywordCount = 0
	
	for keyword in keywords:
		if counts.has_key(keyword):
			keywordCounts.append([keyword, counts[keyword]])
			keywordTotalCount += counts[keyword]
		else:
			keywordCounts.append([keyword, 0])			
		if keyword != 'n/a':
			keywordCount += 1
	kwics = kwic(fileName, keywords)		
	return [keywordCounts, keywordTotalCount, keywordCount, wordCount, kwics]
	

###############################################################################################################################
if os.path.isfile(path + '/count.csv'):
	os.remove(path + '/count.csv')
if os.path.isfile(path + '/kwic.csv'):
	os.remove(path + '/kwic.csv')
read_dictionary()
for dirName in os.listdir(path + '/txt/'):
	ctrcode = dirName
	for year in os.listdir(path + '/txt/' + dirName):
		for manif in os.listdir(path + '/txt/' + dirName +'/'+ year):
			fpath = path+'/txt/'+ dirName + '/'+ year + '/' + manif
			keywordCounts, keywordTotalCount, keywordCount, wordCount, kwics = find_keywords(dictionary[ctrcode], fpath)
			write_csv(keywordCounts, keywordTotalCount, keywordCount, wordCount, fpath)								     
			write_kwic_csv(keywordCounts, kwics, fpath)
			
			
	

#sys.exit() #stop file here
