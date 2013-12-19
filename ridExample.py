# example for RID parser

import nltk
import os
import string
import ridParser
import quanteda
import random

path = '~/Dropbox/QUANTESS/corpora/iebudgets/budget_2010/'
path = os.path.expanduser(path)		# get machine independent path
iebud=quanteda.Corpus(path)			# a Corpus is a list of documents
iebud.preprocess()

# load the dictionary using rid.py
rid = ridParser.RegressiveImageryDictionary()
rid.load_dictionary_from_string(ridParser.DEFAULT_RID_DICTIONARY)
rid.load_exclusion_list_from_string(ridParser.DEFAULT_RID_EXCLUSION_LIST)


data =[]
for speech in iebud.documents:
	# set the class label according to filename
	if "Green" in speech.fname or "FF" in speech.fname:
		speech.variable = "GOV"
	else:
		speech.variable = "OPP"
	# get a dictionary of category counts from rid
	cat_counts = (rid.analyze(speech.text).category_count)
	thisDoc = (cat_counts, speech.variable)
	data.append(thisDoc)


# 'data' is now the format nltk classifiers expect: a list of tuples
#  each element is: (dictionary_of_category_counts, class__label)
# we now shuffle it and split it into 9 training and examples, the rest test
trainData = data[:9]
testData = data[9:]
classifier = nltk.NaiveBayesClassifier.train(trainData)
# regressive imagery doesn't appear ot predict gov or opp very well!
print nltk.classify.accuracy(classifier, testData)




neg_path = '~/Dropbox/QUANTESS/corpora/movieReviews/smaller/neg/'
neg_path = os.path.expanduser(neg_path)		# get machine independent path
pos_path = '~/Dropbox/QUANTESS/corpora/movieReviews/smaller/pos/'
pos_path = os.path.expanduser(pos_path)		# get machine independent path


movies=quanteda.Corpus()			# a Corpus is a list of documents
# add and label the negative reviews
negs = movies.read_docs(neg_path)
movies.add_docs(negs)
for doc in movies.documents:
	if not doc.variable: doc.variable='neg'

# add and label the postive reviews
pos = movies.read_docs(pos_path)
movies.add_docs(pos)
for doc in movies.documents:
	if not doc.variable: doc.variable='pos'
movies.preprocess()

random.shuffle(movies.documents)

data =[]
all_words = set()
#for movie in movies.documents: all_words.update(movie.text)
for movie in movies.documents:
	toks = nltk.tokenize.word_tokenize(movie.text)
	fdist = nltk.FreqDist(toks)
	for x in fdist:
		if fdist[x] > 1: fdist[x]=True
		else: fdist[x]=False
		#print x
		#print fdist[x]
	curDoc = (fdist, movie.variable)

	data.append(curDoc)

trainData = data[:900]
testData = data[900:]
classifier = nltk.NaiveBayesClassifier.train(trainData)
# regressive imagery doesn't appear ot predict gov or opp very well!
print nltk.classify.accuracy(classifier, testData)
print classifier.show_most_informative_features()