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
		"""Load documents from a directory"""
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

	def make_fvms(self):
		data=[]
		for doc in self.documents:
			this_data=doc.make_fvm()
			data.append(this_data)
		self.fvms=data
		return
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
		self.fvm=()

	def __str__(self):
		return "fname: %s variable: %s " % (self.fname, self.variable)


	def preprocess(self):
		"""downcase and remove punctuation"""
		self.text = self.text.lower()
		self.text = self.text.translate(None, string.punctuation)

	def make_fvm(self):
		"""make a feature value matrix (wordtype:frequency)"""
		feat_dict={}
		words = self.text.split()
		for w in words:
			if w in feat_dict:
				feat_dict[w]+=1.0
			else:
				feat_dict[w]=1.0
		self.fvm=feat_dict
		return self.fvm
