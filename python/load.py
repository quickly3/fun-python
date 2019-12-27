import pickle
import csv
import json
import re
import sys
import pandas as pd


def gender_features(word):
    word = word.lower()

    p = {'last_letter': word[-1], 'name': word.lower()}

    if len(word) > 1:
        p['last_2letter'] = word[-2:]

    if len(word) > 2:
        p['last_3letter'] = word[-3:]

    return p


def sp_gender(n, g):

    if n.lower() in sp_male:
        g = "Male"

    if n.lower() in sp_female:
        g = "Female"

    return g


def getMF(df, name, cache):
    name = name.replace("\"", "")

    Male = df.query('given_name =="'+name+'"').query('gender =="Male"')
    Female = df.query('given_name =="'+name+'"').query('gender =="Female"')

    Male = Male['size'].iloc[0] if not (Male.empty) else 0
    Female = Female['size'].iloc[0] if not (Female.empty) else 0

    mf = str(Male) + "|"+str(Female)
    return mf


with open('gender_200w_classifier.pickle', 'rb') as f:
    classifier = pickle.load(f)

classifier.show_most_informative_features(10)


# print(classifier.prob_classify(gender_features("Toni")).prob("Male"))
# print(classifier.prob_classify(gender_features("Toni")).prob("Female"))
# sys.exit()
cache1 = {}
cache2 = {}

testing_names = []

sp_male = ['Alex', 'Alexis', 'Ali', 'Angel', 'Antoine', 'Ara', 'Archie', 'Arya', 'Bala', 'Barrie', 'Bernie', 'Billy', 'Blaine', 'Blane', 'Britt', 'Carey', 'Carmine', 'Casey', 'Charlie', 'Chris', 'Cole', 'Constantine', 'Cory', 'Craig', 'D.', 'Dale', 'Dane', 'Dani', 'Darcy', 'Daryle', 'David', 'Devon', 'Dominique', 'Donnie', 'DORIS ', 'Duane', 'E.', 'Emeka', 'Emile', 'Ernie', 'Etienne', 'Eugene', 'Ezra', 'Gene', 'Ilya', 'Ira', 'Jaime', 'James', 'Jamie', 'Jan', 'Jarret', 'Jean', 'Jeetu', 'Jimmie', 'John', 'Jonah', 'Jordan', 'Judah', 'Karman', 'Kerry',
           'Kris', 'Krishna', 'Kyle', 'L.', 'Lane', 'Lee', 'Leigh', 'Lonnie', 'Loren', 'M.', 'Mani', 'Marty', 'Michal', 'Mickey', 'Mike', 'MJ', 'Morgan', 'Naga', 'Nagendra', 'Nate', 'Neil', 'Nima', 'Partha', 'Pat', 'Peter', 'R.', 'Raja', 'Rajendra', 'Rama', 'Ramy', 'Reese', 'Regan', 'Reggie', 'René', 'Reza', 'Richie', 'Ritchie', 'Robbie', 'Robert', 'Robin', 'Ronnie', 'Royce', 'Rusty', 'Ryan', 'S.', 'Shane', 'Shawn', 'Shayne', 'Shiva', 'Siva', 'Sri', 'Srinivasa', 'Stéphane', 'Surya', 'Sydney', 'Taylor', 'Terry', 'Thomas', 'Tolga', 'Wally', 'Willie', 'Zane', 'Zia']
sp_male = list(map(lambda x: x.lower(), sp_male))
sp_female = ['Alix', 'Amy', 'Andrea', 'Ashley', 'Bev', 'Brenda', 'Bryony', 'Carmel', 'Carmen', 'Carol', 'Catherine', 'Christin', 'Christine', 'Courtenay', 'Courtney', 'Dana', 'Debra', 'Diane', 'Dolores', 'Doris', 'Elizabeth', 'Erin', 'Eve', 'Fran', 'Gale', 'Genevieve', 'Gillian', 'Ginger', 'Ingrid', 'Iris', 'Janet', 'Janis', 'Jennifer', 'Jenny', 'Jillian', 'Jing', 'Jody', 'Karen', 'Kate', 'Kathryn', 'Kelley', 'Kelly', 'Kim', 'Kimberly', 'Kirti', 'Kristen',
             'Laura', 'Laurel', 'Laurie', 'Leslie', 'Linda', 'Lindsay', 'Lisa', 'Liz', 'Lois', 'Lori', 'Lourdes', 'Lynn', 'Maeve', 'Maria', 'Marian', 'Mary', 'Maureen', 'Melissa', 'Mercedes', 'Michelle', 'Miriam', 'Mj', 'Monica', 'Nan', 'Nancy', 'Natalie', 'Patricia', 'Phyllis', 'Rachael', 'Raquel', 'Rupal', 'Sandra', 'Sandy', 'Sarah', 'Sasha', 'Shannan', 'Shannon', 'Siobhan', 'Stacey', 'Stacy', 'Sue', 'Summer', 'Susan', 'Tamar', 'Toni', 'Tracy', 'Trish', 'Vivian', 'Yael']
sp_female = list(map(lambda x: x.lower(), sp_female))


solr_df = pd.read_csv("solr12w.csv", names=[
    "given_name", "gender", "name", "docid", "media", "avatar"])

solr_gp = solr_df.groupby(by=['given_name', 'gender'])

df1 = solr_gp.size().to_frame('size')
df1.reset_index(inplace=True)

ciq_df = pd.read_csv("200w.csv", names=[
    "given_name", "gender", "name", "docid", "media"])


ciq_gp = ciq_df.groupby(by=['given_name', 'gender'])
df2 = ciq_gp.size().to_frame('size')
df2.reset_index(inplace=True)

with open("solr12w.csv", "r") as csvfile:

    lines = csv.reader(csvfile)
    counter = 0

    for line in lines:
        counter += 1
        print(str(counter))
        n = line[0]
        g_o = line[1]
        g_n = "error"

        if len(n) > 0:
            g_n = classifier.classify(gender_features(n))

        diff = "f"

        if g_o.strip() == "":
            diff = "t"
        else:
            if (g_o.lower() != g_n.lower()):
                g_n = sp_gender(n, g_n)
                if(g_o.lower() != g_n.lower()):
                    diff = "t"

        if "t" == diff:

            name_full = line[2]
            docid = "https://research.titanhouse.com/#/candidate/docid/" + \
                line[3]
            media = line[4].strip()
            media = line[4].strip()

            if media != "":
                media = "["+re.sub(r'\\', '', media)+"]"
                media = json.loads(media)
                media = media[0]['link']

            mf1 = getMF(df1, n, cache1)
            mf2 = getMF(df2, n, cache2)
            avatar = line[5].strip()
            testing_names.append(
                (n, g_o, g_n, mf1, mf2, diff, name_full, docid, avatar, media))


with open("solr200w_12w_completed.csv", "w") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["given_name", "gender_old",
                     "gender_predict", "solr M/F", "ciq M/F", "diff", "name", "docid", "avatar", "media"])
    writer.writerows(testing_names)
