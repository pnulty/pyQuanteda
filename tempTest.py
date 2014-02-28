import os
import gensim
import string
import nltk
import quanteda
import codecs
import sys


def fuzzy_match(asterisk, word):
	match = False
	if asterisk[-1] == '*' and asterisk[0] == "*":
	                if asterisk[1:-1] in word: match = True
	elif asterisk[-1] == '*':
	                if word[0:(len(asterisk)-1)] == asterisk[0:-1]: match = True
	elif asterisk[0] == "*":
	                if word[-(len(asterisk)-1):] == asterisk[1:]: match = True
	else:
	                if asterisk==word: match = True
	return match



def read_dictionary(path):
	""" Kohei's dictreading function"""
	dictionary={}
	f = codecs.open(path, 'r', 'utf-8-sig')
	lines=f.readlines()
	f.close()
	for line in lines:
		if line[0] != '#' and len(line.strip()):
			line = line.replace(';', ',')
			label = line.strip().split(':')[0].split(',')
			words = line.strip().split(':')[1].split(',')
			words = [unicode(w.strip())   for w in words]
			dictionary[label[2]] = words
	return(dictionary)



manifs=quanteda.Corpus()

path="/home/paul/Dropbox/populism/"

for ctrcode in os.listdir(path + '/txt/'):
	for year in os.listdir(path + '/txt/' + ctrcode):
		for manif in os.listdir(path + '/txt/' + ctrcode +'/'+ year):
			text = open(path+'/txt/'+ ctrcode + '/'+ year + '/' + manif).read()
			d = quanteda.Document(text, fname=manif, variables={"year":year, "country":ctrcode})
			if d.variables['country']=="IRL":
				d.preprocess()
				manifs.add_docs([d])


popwords = read_dictionary('/home/paul/Dropbox/populism/dictionary.txt')


for d in manifs.documents:
	popcounts = 0
	nonpopcounts = 0 
	words = d.text.split()
	for w in words:
		match=False
		for pw in popwords[d.variables['country']]:
			#print pw
			#print w
			if fuzzy_match(pw, w):
				popcounts+=1
				match=True
				break
		if not match: nonpopcounts+=1

	print d.fname
	print d.variables
	print popcounts
	print nonpopcounts
	print