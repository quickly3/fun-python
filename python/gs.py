

from collections import Counter
from nltk.corpus import names
import random,nltk
import csv
import pandas as pd


def gender_features(word):
    word = word.lower();

    p = {'last_letter':word[-1],'name':word.lower()}

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

testing_names = []
counter = 0

names_freq = Counter()

sp_male = ['Aditya','Ali','Andy','Ari','Bernie','Billy','Bobby','Bradley','Bret','Bryce','Casey','Charlie','Cody','Cole','Dale','Dana','Dane','Darren','Darryl','Daryl','Duane','Dwayne','Eddie','Eli','Enrique','Ernie','Eugene','Gene','Ilya','Ira','Jaime','Jamie','Jesse','Jimmy','Jody','Jose','Karen','Kenneth','Krishna','Kyle','Lee','Leigh','Lonnie','Loren','Luca','Lyle','Maurice','Murali','Nate','Naveen','Oren','Randy','Rene','Rishi','Rocky','Rodney','Ronnie','Rudy','Rusty','Sandy','Seth','Shane','Shannon','Sidney','Stanley','Stephane','Tommy','Tracy','Ty','Warren','Wayne','Wesley','Terry','Shawn',"Chris"]
sp_male = list(map(lambda x: x.lower(), sp_male))
sp_female = ["Abigail","Alexis","Alison","Allison","Allyson","Alyson","Angel","Audrey","Caitlin","Carey","Cathy","Constance","Crystal","Dawn","Deb","Dorothy","Eleanor","Ellen","Erin","Faith","Frances","Gail","Gillian","Ginger","Gretchen","Gwen","Heather","Helen","Hilary","Hillary","Ingrid","Iris","Jan","Janis","Jean","Jenn","Jenny","Jill","Jillian","Jo","Judith","Karin","Kathy","Kerry","Kim","Kris","Kristin","Lillian","M.","Marian","Marion","Mary","Meg","Megan","Meghan","Meredith","Pam","Pat","Penny","Phyllis","Rachel","Robin","Rosemary","Sharon","Sherry","Trish","Vivian","Andrea","Ashley",'Kelly','Leslie','Lisa','Lynn']
sp_female = list(map(lambda x: x.lower(), sp_female))


with open("solr9w.csv","r") as csvfile: 
    lines = csv.reader(csvfile)
    for line in lines:
        n = line[0]

        g_o = line[1]
        g_n = "error"
        if len(n) > 0:
            g_n = classifier.classify(gender_features(n))

        diff = "f"

        if (g_o.lower() != g_n.lower()):
            # g_n = sp_gender(n,g_n)
            # if( g_o.lower() != g_n.lower()):
                diff = "t"
                counter= counter+1
            


        testing_names.append((n,g_o,g_n,diff))



with open("solr200w_9w_completed.csv","w") as csvfile: 
    writer = csv.writer(csvfile)
    writer.writerow(["name","gender_old","gender_predict","diff"])
    writer.writerows(testing_names)



import pickle
f = open('gender_200w_classifier.pickle', 'wb')
pickle.dump(classifier, f)
f.close()



# print(classifier.classify(gender_features("Mary")))

# classifier.show_most_informative_features(20)