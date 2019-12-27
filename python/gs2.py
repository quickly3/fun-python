

from collections import Counter
from nltk.corpus import names
import random,nltk
import csv
import pandas as pd

def gender_features(word):
    word = word.lower();

    p = {'name':word.lower()}

    if len(word) > 1:
        p['last_2letter'] = word[-2:]

    if len(word) > 2:
        p['last_3letter'] = word[-3:]

    return p

def sp_gender(n,g):

    if n.lower() in sp_male:
        g = "Male"

    if n.lower() in sp_female:
        g = "Female"

    return g



names = []
with open("200w.csv","r") as csvfile: 
    lines = csv.reader(csvfile)
    for line in lines:
        n = line[0]
        g = line[1]
        if len(n) > 0:
            names.append((n,g))

random.shuffle(names) 


featuresets = [(gender_features(n),g) for (n,g) in names]

train_set,test_set = featuresets,featuresets

classifier = nltk.NaiveBayesClassifier.train(train_set)

classifier.show_most_informative_features(10)

print(nltk.classify.accuracy(classifier,test_set))



# print(classifier.classify(gender_features("Mary")))

# classifier.show_most_informative_features(20)