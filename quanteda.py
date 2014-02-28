import os
import string
#import nltk
import re
import codecs
#from pandas import Series, DataFrame
#import pandas as pd
class Corpus(object):
        """A grouping of documents and associated data"""

        def __init__(self, path=None):
                if not path==None:
                        self.documents = self.read_docs(path)
                else:
                        self.documents = []
                        self.words = []
                        self.vocab = []
                        #self.fdist = nltk.FreqDist()

        def read_docs(self, path, variables=None):
                """Load documents from a directory and append to corpus"""
                docs=[]
                fnames = os.listdir(path)
                for fname in fnames:
                        f =  codecs.open(os.path.join(path,fname), encoding='utf-8', mode='r')
                        text = f.read()
                        d = Document(text, fname)
                        if variables is not None: d.add_variables(variables)
                        docs.append(d)
                return(docs)

        def add_docs(self, *args):
                """append a list of documents to the corpus"""
                self.documents.extend(args)

        def preprocess(self):
                """ preprocesses every document in the corpus"""
                for doc in self.documents:
                        doc.preprocess()

        def make_fdist(self):
                fdist = nltk.FreqDist()
                for doc in self.documents:
                        toks = nltk.tokenize.word_tokenize(doc.text)
                        doc.words = toks
                        self.fdist.update(toks)
                self.vocab.extend(self.fdist.keys())
                return fdist

        def make_dfm(self):
                """ Make a document term (or document feature) matrix.
                nltk.tokenize is quite slow, so using ordinary .split()
                """
                fdist = nltk.FreqDist()
                for doc in self.documents:
                        #toks = nltk.tokenize.word_tokenize(doc.text)
                        toks = doc.text.split()
                        self.fdist.update(toks)
                self.vocab.extend(self.fdist.keys())
                return fdist

        def __str__(self):
                s=""
                for d in self.documents:
                        s=s+"fname: %s variables: %s \n" % (d.fname, d.variables)
                return s

class Document(object):
        """A document associated with a dictionary of variables"""

        def __init__(self, text, fname, variables={}):
                self.text=text
                self.fname=fname
                self.variables=variables

        def __str__(self):
                return "fname: %s variables: %s " % (self.fname, self.variables)


        def preprocess(self):
                """downcase and remove punctuation"""
                self.text = self.text.lower()
                self.text=re.sub("[\.\t\,\:;\(\)\.\?\"\'']", "", self.text, 0, 0)
                self.text.strip()

        def add_variables(self, new_vars):
                self.variables.update(new_vars)

        def make_dfm(self, target="missing"):
                """make a word frequency matrix (wordtype:frequency Dict)"""
                feat_dict={}
                words = self.text.split()
                for w in words:
                        if w in feat_dict:
                                feat_dict[w]+=1
                        else:
                                feat_dict[w]=0
                data=(feat_dict, self.variables[target])
                return data