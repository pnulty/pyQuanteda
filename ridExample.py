# example for RID parser

import nltk
import os
import sys
import string
import ridParser
import quanteda
import random

# load the dictionary using rid.py
rid = ridParser.RegressiveImageryDictionary()
rid.load_dictionary_from_string(ridParser.DEFAULT_RID_DICTIONARY)
rid.load_exclusion_list_from_string(ridParser.DEFAULT_RID_EXCLUSION_LIST)


neg_path = '~/Dropbox/QUANTESS/corpora/movieReviews/smaller/neg/'
neg_path = os.path.expanduser(neg_path)		# get machine independent path
pos_path = '~/Dropbox/QUANTESS/corpora/movieReviews/smaller/pos/'
pos_path = os.path.expanduser(pos_path)		# get machine independent path

movies=quanteda.Corpus()			# a Corpus has a list of documents

# add and label the negative reviews
negs = movies.read_docs(neg_path, {"sent":"neg"})
movies.add_docs(negs)
# add and label the postive reviews
pos = movies.read_docs(pos_path, {"sent":"pos"})
movies.add_docs(pos)
movies.preprocess()
random.shuffle(movies.documents)


all_cats = {}
for mov in movies.documents:
	thisCats = rid.analyze(mov.text).category_count
	all_cats.update(thisCats)


data=[]
for mov in movies.documents:
	curFeats = dict(zip(all_cats.keys(), [False for k in range(0,len(all_cats.keys()))]))  
	thisCats = rid.analyze(mov.text).category_count
	for x in thisCats:
		if thisCats[x] > 1 and x in curFeats.keys(): curFeats[x]=True
	print curFeats
	data.append( (curFeats, mov.variables["sent"]))
random.shuffle(data)
trainData = data[0:1600]
testData = data[400:]
classifier = nltk.NaiveBayesClassifier.train(trainData)
print nltk.classify.accuracy(classifier, testData)
print classifier.show_most_informative_features()

