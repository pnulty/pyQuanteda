import nltk
import os
import quanteda
import random
import zipfile
from nltk.classify import SklearnClassifier
from sklearn.naive_bayes import BernoulliNB
from sklearn.svm import SVC

leftParties = ["Laba", "Lab", "Lib", "Comm", "LibSDP", "SF", "SEP", "TW", "Gr", "Resp"]

ukMan=quanteda.Corpus()
with zipfile.ZipFile("/home/paul/UK_Manifestos.zip") as myzip:
	for n in myzip.namelist():
		d = quanteda.Document(myzip.open(n).read(), n)
		ukMan.documents.append(d)
		n = n.replace('Con_a', 'Cona')
		n = n.replace('Lab_a', 'Laba')
		n = n.replace('.txt', '')
		v = n.split('_')
		wing = "None"
		if v[4] in leftParties: wing = "Left"
		else: wing = "Right"
		d.add_variables({"elecType":v[1], "year":v[2], "lang":v[3], "party":v[4], "wing":wing  }  )

ukMan.preprocess()

fdist = ukMan.make_fvm()

data =[]
for man in ukMan.documents:
	curFeats = dict(zip(fdist.keys()[0:500], [False for k in range(0,500)] ))
	toks = nltk.tokenize.word_tokenize(man.text)
	curDist = nltk.FreqDist(toks)
	for x in curDist:
		if curDist[x] > 2 and x in curFeats.keys(): curFeats[x]=True
	data.append( (curFeats, man.variables["wing"]) )
random.shuffle(data)
trainData = data[0:85]
testData = data[85:]
classifier = nltk.NaiveBayesClassifier.train(trainData)
print nltk.classify.accuracy(classifier, testData)
print classifier.show_most_informative_features()
classifier = nltk.DecisionTreeClassifier.train(trainData)
print nltk.classify.accuracy(classifier, testData)