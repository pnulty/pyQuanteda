from sklearn.naive_bayes import GaussianNB
from sklearn.feature_extraction import DictVectorizer
import numpy as np
import os
import ridParser

path = '~/Dropbox/QUANTESS/corpora/iebudgets/budget_2010/'
path = os.path.expanduser(path)		# get machine independent path
fnames = os.listdir(path)
docs = []
labels = []
for fname in fnames:
        f = open(os.path.join(path,fname))
        text = f.read()
        docs.append(text)
        label = "GOV" if "Green" in fname or "FF" in fname else "OPP"
    	labels.append(label)

# load the dictionary using rid.py
rid = ridParser.RegressiveImageryDictionary()
rid.load_dictionary_from_string(ridParser.DEFAULT_RID_DICTIONARY)
rid.load_exclusion_list_from_string(ridParser.DEFAULT_RID_EXCLUSION_LIST)

data =[]
vec = DictVectorizer()
for speech in docs:
	# get a dictionary of category counts from rid
	cat_counts = (rid.analyze(speech).category_count)
	for x in cat_counts:
		print x
		print cat_counts[x]

	cat_counts = vec.fit_transform(cat_counts).toarray()
	print(type(cat_counts))
	data.append(cat_counts.flatten())

clf = GaussianNB()
data = np.array(data)
labels = np.array(labels)

print
print

for d in data: print(d.shape)
for d in labels: print(d.shape)
clf.fit(data[0:5], labels[0:5])
#print(clf.predict(data[5:10]))