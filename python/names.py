#!/usr/bin/python
# -*- coding: UTF-8 -*- 


def gender_features(word):
	return {'last_letter':word[-1]}


from nltk.corpus import names
import random,nltk
names = ([(name,'male') for name in names.words('male.txt')] + [ (name, 'female') for name in names.words('female.txt')])

random.shuffle(names) 

featuresets = [(gender_features(n),g) for (n,g) in names]
train_set,test_set = featuresets[500:],featuresets[:500]
classifier = nltk.NaiveBayesClassifier.train(train_set)

print(nltk.classify.accuracy(classifier,test_set))
print(classifier.classify({'last_letter': 'a'}))
classifier.show_most_informative_features(5)