import os
import gensim
import string
import nltk
import quanteda
import codecs
import sys
import glob


def wildcard_match(asterisk, word):
	""" match wildcards indicated with asterisks"""
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

path="/home/paul/Dropbox/QUANTESS/corpora/UK Manifestos/"

files=os.listdir(path)
for fname in files:
	f = open(path+fname, 'r')
	text=f.read()
	text = text.decode('latin1')
	temp=fname.split('_')
	country=temp[0]
	year = temp[2]
	party=temp[4].replace('.txt','')
	d=quanteda.Document(text, fname=fname, variables={"year":year, "country":country, "party":party})
	d.preprocess()
	manifs.add_docs([d])

print manifs




popwords = read_dictionary('/home/paul/Dropbox/populism/dictionary.txt')


for d in manifs.documents:
	popcounts = 0
	nonpopcounts = 0 
	words = d.text.split()
	for w in words:
		match=False
		for pw in popwords[d.variables['country']]:
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