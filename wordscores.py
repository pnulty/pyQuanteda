from quanteda import *

class Wordscores(object):
	def __init__(self):
		#dictionaries mapping features and classes to their priors
		self.classes={}

	def train(self, train_corp):
		sumfwrs = {}
		for doc in train_corp.documents:
			doc.fwrs={x:(doc.fvm[x]/len(doc.fvm)) for x in doc.fvm}
			for f in doc.fwrs:
				sumfwrs[f] = sumfwrs.get(f,doc.fwrs[f])+doc.fwrs[f]
		for doc in train_corp.documents:
			doc.pwrs = {x:(doc.fwrs[x]/sumfwrs[x]) for x in doc.fwrs}
		wordscores = {}
		for doc in train_corp.documents:
			for p in doc.pwrs:
				print doc.pwrs[p]
				if p in wordscores:
					wordscores[p]=wordscores[p]+(doc.pwrs[p]*doc.variable)
				else:
					wordscores[p]=(doc.pwrs[p]*doc.variable)
		return wordscores
		

	def test(self, fvms):
		pass

path = '~/Dropbox/QUANTESS/corpora/iebudgets/budget_2010/'
path = os.path.expanduser(path)

iebud10=Corpus(path)
iebud10.preprocess()
for d in iebud10.documents:
	if "Green" in d.fname or "FF" in d.fname:
		d.variable = -1.0
	else:
		d.variable = 1.0

train_corp=Corpus()
test_corp=Corpus()
train_corp.add_docs(iebud10.documents[0:2])
test_corp.add_docs(iebud10.documents[2:])
train_corp.make_fvms()
w = Wordscores()
scores = w.train(train_corp)
print scores
#test_fvms=test_corp.make_fvm()
