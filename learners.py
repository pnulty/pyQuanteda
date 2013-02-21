from quanteda import *
import math

class NaiveBayes(object):
	def __init__(self):
		#dictionaries mapping features and classes to their priors
		self.classes={}
		self.class_priors={}
		self.feature_priors={}
		self.feat_class_priors={} 

	def make_priors(self,data):
		#make the class priors
		for d in data:
			this_class=d[1]
			if this_class in self.classes:
				self.classes[this_class] += 1.0
			else:
				self.classes[this_class] = 1.0
		for c in self.classes:
			self.class_priors[c] = self.classes[c]/len(self.classes)

		#make the feature priors
		feature_counts={}
		for d in data:
			feats=d[0]
			for f in feats:
				if f in feature_counts:
					feature_counts[f]+=feats[f]
				else:
					feature_counts[f]=feats[f]
			s=sum(feature_counts.values())
			for c in feature_counts: self.feature_priors[c]=(feature_counts[c]/s)

	def train(self, data):
		#count and normalize feature:class co-occurrences
		self.make_priors(data)
		feat_class_counts={}
		for feat in self.feature_priors.keys():
			feat_class_counts[feat]=dict( (c, 0.0) for c in self.classes)
		for d in data:
			features=d[0]
			c=d[1]
			for f in features:
				if not c in feat_class_counts[f]:
					feat_class_counts[f][c]=features[f]
				else:
					feat_class_counts[f][c]+=features[f]
		for x in feat_class_counts:
			for y in feat_class_counts[x]:
				feat_class_counts[x][y]=feat_class_counts[x][y]/len(self.feature_priors)
		self.feature_class_priors=feat_class_counts


	def test(self, data):
		"""sum log probabilities for classes given features in test data"""
		unseen=0
		for d in data:
			feats=d[0]
			true_class=d[1]
			probs={}
			preds={}
			for c in self.classes:
				probs[c]=0
				preds[c]=0
			for f in feats:
				for c in self.classes:
					if f in self.feature_class_priors.keys():
						temp=self.feature_class_priors[f][c]
						if not temp == 0:
							probs[c]+=(-math.log(temp))
					else:
						unseen+=1
			for c in probs:
				#print probs[c]
				preds[c]=probs[c]/self.class_priors[c]
			ratio = preds["GOV"]/preds["OPP"]
			print true_class
			print ratio
			print preds
			print "\n"



path = '/home/paul/Dropbox/QUANTESS/corpora/iebudgets/budget_2010'

iebud=Corpus(path)
iebud.preprocess()


for d in iebud.documents:
	if "Green" in d.fname or "FF" in d.fname:
		d.variable = "GOV"
	else:
		d.variable = "OPP"

train_corp=Corpus()
test_corp=Corpus()
train_corp.add_docs(iebud.documents[0:2])
test_corp.add_docs(iebud.documents[2:])

print "training: "
for d in train_corp.documents:
	print d

print "testing: "
for d in test_corp.documents:
	print d

train_data=train_corp.make_fvm()
test_data=test_corp.make_fvm()

data=iebud.make_data()
nb=NaiveBayes()
nb.train(train_data)
print nb.classes
print nb.class_priors

nb.test(test_data)

