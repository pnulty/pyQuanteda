from sklearn.naive_bayes import GaussianNB
import numpy as np


path = '~/Dropbox/QUANTESS/corpora/iebudgets/budget_2010/'
path = os.path.expanduser(path)		# get machine independent path
fnames = os.listdir(path)
docs = []
labels =[]
for fname in fnames:
        f = open(os.path.join(path,fname))
        text = f.read()
        docs.append(text)
        label = "GOV" if "Green" in fname or "FF" in fname: else "OPP"
    	labels.append(label)

# load the dictionary using rid.py
rid = ridParser.RegressiveImageryDictionary()
rid.load_dictionary_from_string(ridParser.DEFAULT_RID_DICTIONARY)
rid.load_exclusion_list_from_string(ridParser.DEFAULT_RID_EXCLUSION_LIST)

data =[]
vec = DictVectorizer()
for speech in docs:
	# set the class label according to filename
	if "Green" in speech.fname or "FF" in speech.fname:
		speech.variable = "GOV"
	else:
		speech.variable = "OPP"
	# get a dictionary of category counts from rid
	cat_counts = (rid.analyze(speech).category_count)
	vec.fit_transform(cat_counts).toarray()
	thisDoc = (cat_counts)
	data.append(thisDoc)

clf = GaussianNB()
clf.fit(data[0:5], lables[0:5])
print(clf.predict(data[5:10])

# 'data' is now the format nltk classifiers expect: a list of tuples
#  each element is: (dictionary_of_category_counts, class__label)
# we now shuffle it and split it into 9 training and examples, the rest test
