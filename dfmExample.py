import os
import gensim
import string
import nltk
import quanteda
import codecs
import sys
import random
import numpy as np


path="/home/paul/Dropbox/populism/"

neg_path = '~/Dropbox/QUANTESS/corpora/movieReviews/smaller/neg/'
neg_path = os.path.expanduser(neg_path)		# get machine independent path
pos_path = '~/Dropbox/QUANTESS/corpora/movieReviews/smaller/pos/'
pos_path = os.path.expanduser(pos_path)		# get machine independent path

movies=quanteda.Corpus()

# add and label the negative reviews
negs = movies.read_docs(neg_path, {"sent":"neg"})
movies.add_docs(*negs)
# add and label the postive reviews
pos = movies.read_docs(pos_path, {"sent":"pos"})
movies.add_docs(*pos)
movies.preprocess()
random.shuffle(movies.documents)
print("1")
movies.make_fdist()
print("2")


dfm = np.zeros((len(movies.documents), len(movies.vocab)))
print len(movies.vocab)
print len(movies.documents)
i=0
while(i<len(movies.documents)):
	print i
	j=0
	while(j<len(movies.vocab)):
		dfm[i,j]=movies.documents[i].words.count(movies.vocab[j])
		j+=1
	i+=1
