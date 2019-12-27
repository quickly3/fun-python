#!/usr/bin/python
# -*- coding: UTF-8 -*- 


from nltk.corpus import PlaintextCorpusReader
from nltk.corpus import stopwords
from nltk import FreqDist
from nltk import PorterStemmer
from operator import itemgetter  
import json
import csv


corpus_root = '/Users/hongbinzhou/python/company_corpus'

en_stopwords = stopwords.words("english")

wordlists = PlaintextCorpusReader(corpus_root, '.*')
# wordlists.fileids()

count = len(wordlists.fileids())

current = 0

main_freq = {};



for w in wordlists.fileids():
	current = current + 1

	print str(current) + "/" + str(count)

	# get corpus
	text = wordlists.words(w)
	# filter stopwords
	text = [w.encode("utf-8") for w in text if w.lower() not in en_stopwords]

	# filter punctuation mark
	text = list([w.lower() for w in text if w.isalpha()])

	#pick up stem
	# porter = PorterStemmer()
	# Google = [porter.stem(w) for w in Google]

	fdist1 = FreqDist(text)

	fd_list = fdist1.items()


	if len(main_freq) == 0 :
		for tup in fd_list:
			main_freq[tup[0]] = 1

	else :
		for new_freq in fd_list: 
			if new_freq[0] in main_freq :
				main_freq[new_freq[0]] = main_freq[new_freq[0]] + 1
			else :
				main_freq[new_freq[0]] = 1


	# if current == 100:
	# 	# for i in main_freq:
	# 		# print i,main_freq[i]
	# 	break
	
# print sorted(main_freq.items(), key=lambda d: d[1])




res = [];

for i in main_freq:
	res.append({'word':i,'count':main_freq[i]}) 


res.sort(key = lambda x:x["count"])


with open("per.csv","w") as csvfile: 
    writer = csv.writer(csvfile)

    #先写入columns_name
    # writer.writerow(["index","a_name","b_name"])
    #写入多行用writerows
    #
    for line in res:

    	writer.writerow([line['word'], line['count']])
    # writer.writerows([[0,1,3],[1,2,3],[2,3,4]])


# file = open("res.txt","w+")

# file.write(str(res));

# print res

# print(sorted(fdist1.items(), key=itemgetter(1))) 


# for item in fdist1.items():
# 	print type(item)