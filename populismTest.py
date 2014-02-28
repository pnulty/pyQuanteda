import os
#import gensim
import string
import nltk
import quanteda
import codecs
import sys
import chardet


def fuzzy_match(asterisk, word):
	match = False
	#print type(asterisk)
	#print type(word)
	if asterisk[-1] == '*' and asterisk[0] == "*":
	    if asterisk[1:-1] in word: match = True
	elif asterisk[-1] == '*':
	    if word[0:(len(asterisk)-1)] == asterisk[0:-1]: match = True
	elif asterisk[0] == "*":
	    if word[-(len(asterisk)-1):] == asterisk[1:]: match = True
	else:
	    if asterisk==word: match = True
	return match



def read_dictionary(path):
	""" Kohei's dictreading function"""
	dictionary={}
	f = codecs.open(path, 'r', 'utf-8-sig')
	lines=f.readlines()
	f.close()
	for line in lines:
		if line[0] != '#' and len(line.strip()):
			line = line.replace(';', ',')
			label = line.strip().split(':')[0].split(',')
			words = line.strip().split(':')[1].split(',')
			words = [unicode(w.strip())   for w in words]
			dictionary[label[2]] = words
	return(dictionary)





def get_docs_folders(path):
	manifs=quanteda.Corpus()
	for ctrcode in os.listdir(path):
		print ctrcode
		for year in os.listdir(path + ctrcode):
			for manif in os.listdir(path+ ctrcode +'/'+ year):
				text = open(path+ ctrcode + '/'+ year + '/' + manif).read()
				res = chardet.detect(text)
				text = text.decode(res['encoding'])
				party = manif.split('_')[0]
				d = quanteda.Document(text, fname=manif, variables={"year":year, "country":ctrcode, "party":party})
				d.preprocess()
				manifs.add_docs(d)
	return manifs


def kwic(words, doc, window=8):
	all_contexts=[]
	for w in words:
		toks = doc.text.split()
		for index in range( len(toks) ):
			context=[]
			if fuzzy_match(w,toks[index]):
				start = max(0, index-window)
				finish = min(len(toks), index+window+1)
				context.append(doc.fname)
				for v in doc.variables: context.append(v+':'+doc.variables[v])
				thisContext=' '.join(toks[start:finish])
				thisContext = thisContext.replace(toks[index], '*'+toks[index]+'*')
				context.append(thisContext)
				#for c in contexts: c=str(c)
				context.append('\n')
				all_contexts.append(context)
				#all_contexts.append('\n')
	return(all_contexts)

popwords = read_dictionary('/home/paul/Dropbox/populism/dictionary.txt')
dicText = open("/home/paul/Dropbox/populism/CMPpartyCodebook.txt").read()

res= chardet.detect(dicText)
legend = {}
leglines = open("/home/paul/Dropbox/populism/CMPpartyCodebook.txt").readlines()
for line in leglines:
	line=unicode(line, encoding=res["encoding"])
	parts=line.split(',')
	temp=parts[2].split(':')
	key = temp[0]
	party = temp[1]
	legend[key]=party

path="/home/paul/Dropbox/populism/utxt/"
manifs = get_docs_folders(path)

for doc in manifs.documents:
	if doc.variables['party'].isdigit():
		try:
			doc.variables['party']=legend[doc.variables['party']]
		except KeyError:
			doc.variables['party']=" "


# f=open('kwic_output.csv', 'w')
# print popwords
# for doc in manifs.documents:
# 	print doc.variables
# 	ac = kwic(popwords[doc.variables['country']], doc )
# 	for c in ac:
# 		f.write(str(c))
# 		f.write('\n')



f=open('percent_output.csv', 'w')
for d in manifs.documents:
	popcounts = 0.0
	nonpopcounts = 0.0 
	words = d.text.split()
	for w in words:
		match=False
		for pw in popwords[d.variables['country']]:
			#print pw
			#print w
			if fuzzy_match(pw, w):
				popcounts+=1.0
				match=True
				break
		if not match: nonpopcounts+=1.0
	print popcounts
	f.write(d.fname + ',')
	for v in d.variables: f.write(v+':' +d.variables[v].encode('utf8', 'replace')+ ',')
	f.write( str(popcounts) +',')
	f.write( str(popcounts+nonpopcounts)+',')
	f.write( str(popcounts/nonpopcounts)+'\n')
	print d.fname
	print d.variables
	print "Populist words:  %f " % (popcounts)
	print "Total words:  %f " % (popcounts+nonpopcounts)
	print "Populist Percentage: %f" % (popcounts/nonpopcounts)
	print

exit()



