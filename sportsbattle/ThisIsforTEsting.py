import os
import csv
full_path = os.path.realpath(__file__)
directory = os.path.dirname(full_path)+"/leagues"
Leaders = []
with open(directory+'/league1.csv', 'r') as csv_file:

    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        NameScore = {'Name': row[0],
                         'Score' : int(row[1])    
                    }
        Leaders.append(NameScore)
Leaders = sorted(Leaders, key = lambda i: i['Score'],reverse=True) 
stef = 5