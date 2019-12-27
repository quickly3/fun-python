#!/usr/bin/python
# -*- coding: UTF-8 -*- 


import nltk
from nltk.corpus import PlaintextCorpusReader
corpus_root = '/Users/hongbinzhou/corpus/company_desc'
wordlists = PlaintextCorpusReader(corpus_root, '.*')
files = wordlists.fileids()

file_words = wordlists.words("test.txt");

for word in file_words:
	print word

# print file_word
# print "你好，世界"