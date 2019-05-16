import os
import csv
os.chdir("D:\\2019 Spring Baruch\Columbia Engineering\Python")
os.getcwd()

with open("cereal-cleaner.csv", newline="") as csvfile:
    csvreader=csv.reader(csvfile, delimiter=",")
    csv_header = next(csvfile)
    print(f'Header: {csv_header}')

    for row in csvreader:
        if float(row[7]) >= 5:
            print(row)