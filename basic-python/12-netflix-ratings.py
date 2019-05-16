import csv

video = input("What show or movie are you looking for? ")
found = False 

with open("netflix_ratings.csv", newline="") as csvfile:
    netflix = csv.reader(csvfile, delimiter=",")
    
    for row in netflix:
        if row[0] == video:
            print(row[0] + " is rated " + row[1] + 
            " with a rating of " + row[5])
            found = True
            break
    
    if found is False:
        print("Sorry, we don't find any match!")
