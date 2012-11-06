import os
import string

class Corpus(object):
	"""A list of documents"""

	def __init__(self, path=None):
		if not path==None:
			self.documents = self.read_docs(path)
		else:
			self.documents = []

	def read_docs(self, path):
		docs=[]
		fnames = os.listdir(path)
		for fname in fnames:
			f = open(os.path.join(path,fname))
			text = f.read()
			d = Document(text, fname, fname)
			docs.append(d)
		return(docs)

	def add_docs(self, docs):
		self.documents.extend(docs)

	def preprocess(self):
		for doc in self.documents:
			doc.preprocess()

	def make_data(self):
		data=[]
		for doc in self.documents:
			this_data=doc.make_data()
			data.append(this_data)
		return data



	def __str__(self):
		s=""
		for d in self.documents:
			s=s+"fname: %s variable: %s \n" % (d.fname, d.variable)
		return s

class Document(object):
	"""A document associated with a single dependent variable"""

	def __init__(self, text, fname, variable=None):
		self.text=text
		self.fname=fname
		self.variable=variable
		self.feature_matrix=()

	def __str__(self):
		return "fname: %s variable: %s " % (self.fname, self.variable)


	def preprocess(self):
		self.text = self.text.lower()
		self.text = self.text.translate(None, string.punctuation)

	def make_data(self):
		feat_dict={}
		words = self.text.split()
		for w in words:
			if w in feat_dict:
				feat_dict[w]+=1
			else:
				feat_dict[w]=0
		data=(feat_dict, self.variable)
		return data

