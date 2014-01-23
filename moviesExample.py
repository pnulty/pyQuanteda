import nltk
import os
import quanteda
import random

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

fdist = movies.make_fvm()
data=[]
for mov in movies.documents:
	curFeats = dict(zip(fdist.keys()[0:1000], [False for k in range(0,1000)] ))
	toks = nltk.tokenize.word_tokenize(mov.text)
	curDist = nltk.FreqDist(toks)
	for x in curDist:
		if curDist[x] > 1 and x in curFeats.keys(): curFeats[x]=True
	print curFeats
	data.append( (curFeats, mov.variables["sent"]))
random.shuffle(data)
trainData = data[0:1500]
testData = data[500:]
classifier = nltk.NaiveBayesClassifier.train(trainData)
print nltk.classify.accuracy(classifier, testData)
print classifier.show_most_informative_features()