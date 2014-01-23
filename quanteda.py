import os
import string
import nltk
class Corpus(object):
        """A list of documents"""

        def __init__(self, path=None):
                if not path==None:
                        self.documents = self.read_docs(path)
                else:
                        self.documents = []

        def read_docs(self, path, variables=None):
                """Load documents from a directory and append to corpus"""
                docs=[]
                fnames = os.listdir(path)
                for fname in fnames:
                        f = open(os.path.join(path,fname))
                        text = f.read()
                        d = Document(text, fname)
                        if variables is not None: d.add_variables(variables)
                        docs.append(d)
                return(docs)

        def add_docs(self, new_docs):
                """append a list of documents to the corpus"""
                self.documents.extend(new_docs)


        def preprocess(self):
                for doc in self.documents:
                        doc.preprocess()

        def make_fvm(self):
                fdist = nltk.FreqDist()
                for doc in self.documents:
                        toks = nltk.tokenize.word_tokenize(doc.text)
                        fdist.update(toks)
                return fdist

        def __str__(self):
                s=""
                for d in self.documents:
                        s=s+"fname: %s variable: %s \n" % (d.fname, d.variable)
                return s

class Document(object):
        """A document associated with a dictionary of variables"""

        def __init__(self, text, fname, variable=None):
                self.text=text
                self.fname=fname
                self.variables={}
                self.feature_matrix=()

        def __str__(self):
                return "fname: %s variable: %s " % (self.fname, self.variables)


        def preprocess(self):
                """downcase and remove punctuation"""
                self.text = self.text.lower()
                self.text = self.text.translate(None, string.punctuation)
                self.text.strip()

        def add_variables(self, new_vars):
                self.variables.update(new_vars)

        def make_fvm(self, target="missing"):
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