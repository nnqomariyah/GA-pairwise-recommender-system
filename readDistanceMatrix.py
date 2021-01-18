import json
import csv
from distanceMatrix import getDestinations


def getDistanceList(filename):
    with open(filename) as f:
        reader = csv.reader(f)
        data = list(reader)
    f.close()
    return data

def getDistance(distanceList, origin, dest):
    destIndex = distanceList[0].index(dest)
    originIndex = distanceList[0].index(origin)
    distance = distanceList[originIndex][destIndex]
    return int(distance)

def getDuration(durationList, origin, dest):
    destIndex = durationList[0].index(dest)
    originIndex = durationList[0].index(origin)
    duration = durationList[originIndex][destIndex]
    return int(duration)

