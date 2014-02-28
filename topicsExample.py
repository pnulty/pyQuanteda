import os
import gensim
import string
import nltk
import quanteda
import codecs
import sys
import random


path="/home/paul/Dropbox/populism/"

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
print movies
movies.add_docs(pos)
movies.preprocess()
random.shuffle(movies.documents)

texts=[]
for m in movies.documents:
	words = m.text.split()
	texts.append(words)

dictionary = gensim.corpora.Dictionary(texts)
corpus = [dictionary.doc2bow(text) for text in texts]
gensim.corpora.MmCorpus.serialize('/tmp/irl.mm', corpus)
corpus = gensim.corpora.MmCorpus('/tmp/irl.mm')

tfidf = gensim.models.TfidfModel(corpus)
corpus_tfidf = tfidf[corpus]
print corpus_tfidf
print dictionary
model = gensim.models.ldamodel.LdaModel(corpus_tfidf, id2word=dictionary, num_topics=20, update_every=0, passes=10)
model.show_topics(20)
for j in model.print_topics(20): print j
