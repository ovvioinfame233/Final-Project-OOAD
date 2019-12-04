
import os

userpass = {'admin': 'admin'}
full_path = os.path.realpath(__file__)
directory = os.path.dirname(full_path)+"/Users"
for filename in os.listdir(directory):
    if filename.endswith(".txt"):
        f = open(directory+"/"+filename)
        UserPassString = f.readline()
        UserPassString = UserPassString.split(",")
        Username = UserPassString[0]
        Password = UserPassString[1]
        userpass[Username] = Password

stef = 14