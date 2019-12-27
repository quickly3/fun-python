import pandas as pd
import csv

name_gender = {}
Males = []
Females = []

with open("male_female.csv","r") as csvfile: 
    lines = csv.reader(csvfile)
    for line in lines:
        if line[0] in name_gender:
            name_gender[line[0]][line[1]] = line[2]
        else:
            name_gender[line[0]] = {line[1]:line[2]}

for item in name_gender:

    if "Male" not in name_gender[item]:
        name_gender[item]["Male"] = 0

    if "Female" not in name_gender[item]:
        name_gender[item]["Female"] = 0

    if int(name_gender[item]["Female"]) > int(name_gender[item]["Male"]):
        Females.append(item);
    else:
        Males.append(item);

# print(name_gender['Andrea'])

# all_names = df['Name'].unique()
# print(df)

# all_names = pd.DataFrame(columns=['name','gender_old','cnt'])
print(Females)
print(Males)
