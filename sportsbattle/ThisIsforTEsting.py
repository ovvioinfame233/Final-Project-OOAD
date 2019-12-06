import os
import csv
full_path = os.path.realpath(__file__)
directory = os.path.dirname(full_path)+"/Users"
Leaders = [["Join a Leauge"],["Join a League"],["Join a League"]]
with open(directory+'/admin.csv', 'r') as csv_file:
    count = 0
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        if(row != [] ):
            Leaders[count] = row
            count = count +1 
stef = 5
real= []
for i in range(len(Leaders)):
    real.append(Leaders[i][0])

setfa =6 