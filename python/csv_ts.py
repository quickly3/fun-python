import csv

names = [];
with open("solr5000.csv","r") as csvfile: 
    lines = csv.reader(csvfile)
    for line in lines:
        n = line[0]
        names.append((n,n[-1],n[-2:],n[-3:]))


with open("solr5000_last_letter.csv","w") as csvfile: 
    writer = csv.writer(csvfile)
    writer.writerow(["name","last1","last2","last3","gender"])
    writer.writerows(names)
