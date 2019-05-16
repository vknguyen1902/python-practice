import os
import csv

def getPercentages(wrestlerData):
    total_matches = wrestlerData[1] + wrestlerData[2] + wrestlerData[3]
    percent_won = (int(wrestlerData[1])/int(total_matches))*100
    
    print(f'Total Matches: {total_matches}')
    print(f'Percent Won: {percent_won}')

with open("wwe-data-2016.csv", newline="") as csvfile:
    wwe = csv.reader(csvfile, delimiter=",")
    print(next(wwe))                    #print the headers
    
    #print(getPercentages(wwe[2]))
    for row in wwe:                     #how about looping by column?
        print(getPercentages(row))