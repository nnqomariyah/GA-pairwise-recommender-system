import googlemaps 
import csv
import json


def getDestinations(filename):
    dests = []
    with open(filename) as csv_file:
        next(csv_file)
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            dests.append(row[1])
        csv_file.close()
    return dests

