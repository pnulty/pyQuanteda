#!/usr/bin/env python

""" Script to convert files of unknown encoding to Unicode

A simple wrapper around two python character detection libraries,
chardet and python-magic. These libraries try to heuristically
detect the encoding of the input files. The files are then encoded using
Python's unicode() function and written to an output folder.

Chardet is slower but returns confidence values and should detect
older Windows encodings better than magic (which uses unix file -ib)

Chardet is used by default, to use libmagic pass 'magic' as the
thrd argument

Guide:

First, install libmagic or chardet or both:

> pip install libmagic

> pip install chardet

Then to detect and change the encoding of a directory of files:

> python make_unicode /path/to/infiles /path/to/outfiles/

or using libmagic:

> python make_unicode /path/to/infiles /path/to/outfiles/ magic


"""
__author__ = 'Paul Nulty <paul.nulty@gmail.com>'
__copyright__ = 'GPL'

import os
import sys
import codecs



__author__ = "Paul Nulty"
__email__ = "paul.nulty@gmail.com>"
__license__ = "GPL"


def chardet_convert(inpath, outpath, verbose=True):
	import chardet
	infiles= os.listdir(inpath)
	for f in infiles:
		rawdata=open(inpath+f,"r").read()
		res= chardet.detect(rawdata)
		if verbose:
			print f
			print res
			print
		if res["encoding"]==None: res["encoding"]='latin-1'
		output = open(inpath+f,"r").read()
		output = unicode(output, encoding=res["encoding"])
		outfile = codecs.open(outpath+f,"w")
		outfile.write(output.encode('utf-8'))

def magic_convert(inpath, outpath, verbose=True):
	import magic
	infiles= os.listdir(inpath)
	for f in infiles:
		blob = open(inpath+f).read()
		m = magic.Magic(mime_encoding=True)
		enc = m.from_buffer(blob)
		if verbose:
			print f
			print enc

		output = open(inpath+f,"r").read()
		try:
			output = unicode(output, encoding=enc, errors="replace")
		except LookupError:
			print "Encoding unknown, writing original file."
			outfile = codecs.open(outpath+f,"w")
			outfile.write(output)
		else:
			outfile = codecs.open(outpath+f,"w")
			outfile.write(output.encode('utf-8'))

if __name__=="__main__":
	if len(sys.argv) < 3:
		print "please specify input and output directories, e.g. python \
		make_unicode.py /path/to/files/ /path/to/output/"
	inp = sys.argv[1]
	out = sys.argv[2]
	if len(sys.argv) < 4:
		chardet_convert(inp,out)
	elif sys.argv[3]=='magic':
		magic_convert(inp,out)
	else:
		print "unknown argument %s" % (sys.argv[3])
