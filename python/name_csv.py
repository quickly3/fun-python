#!/usr/bin/python
# -*- coding: UTF-8 -*- 


def gender_features(word):
	return {'last_letter':word[-1]}


from nltk.corpus import names
import random,nltk
import csv

names = ([(name,name[-1],name[-2:],'male') for name in names.words('male.txt')] + [ (name,name[-1],name[-2:], 'female') for name in names.words('female.txt')])

random.shuffle(names) 


with open("names_last_letter.csv","w") as csvfile: 
    writer = csv.writer(csvfile)
    writer.writerow(["name","last1","b_name"])
    writer.writerows(names)


# featuresets = [(gender_features(n),g) for (n,g) in names]
# train_set,test_set = featuresets[500:],featuresets[:500]
# classifier = nltk.NaiveBayesClassifier.train(train_set)

# print nltk.classify.accuracy(classifier,test_set);
# print(classifier.classify({'last_letter': 'a'}))
# classifier.show_most_informative_features(5)