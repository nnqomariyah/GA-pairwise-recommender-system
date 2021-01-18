#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 19:15:56 2020

@author: nungqee.york
"""

from utils import *
from routeOptimizer import RouteOptimizer
from readDistanceMatrix import getDistanceList
import time
import getopt, sys 
start = time.process_time()

nPeople = 2
budget = 3000000
duration = 3
epochs = 400
#genePool = readJson("jsonAttraction.txt")
#dList = getDistanceList('distanceMatrix.csv')
#durList = getDistanceList('durationMatrix.csv')

genePool = readJsonV2("jsonAttraction.txt")
dList = getDistanceList('distanceMatrix.csv')
durList = getDistanceList('durationMatrix.csv')
TAGS = ['museum','beach','kids-friendly']


# Remove 1st argument from the 
# list of command line arguments 
argumentList = sys.argv[1:] 

options = "g:l:r:p:b:d:e:t:"
long_options = ["genePool=", "dList=", "durList=","nPeople=","budget=","duration=","epochs=",'tags='] 
  


try: 
    # Parsing argument 
    arguments, values = getopt.getopt(argumentList, options, long_options) 
      
    # checking each argument 
    for currentArgument, currentValue in arguments:   
        
        if currentArgument in ("-g", "--genePool"): 
            genePool = readJson(currentValue)
            
        elif currentArgument in ("-l", "--dList"): 
            dList = getDistanceList(currentValue) 
              
        elif currentArgument in ("-r", "--durList"): 
            durList = getDistanceList(currentValue) 
            
        elif currentArgument in ("-p", "--nPeople"): 
            nPeople=int(currentValue)
        
        elif currentArgument in ("-b", "--budget"): 
            budget=int(currentValue)
        
        elif currentArgument in ("-d", "--duration"): 
            duration=int(currentValue)
            
        elif currentArgument in ("-e", "--epochs"): 
            epochs=int(currentValue)
        
        elif currentArgument in ("-t", "--tags"): 
            TAGS = [c for c in currentValue.split(',')] 
            print (TAGS)
            #TAGS = ['museum','beach','kids-friendly']
        
              
except getopt.error as err: 
    # output error, and return with an error code 
    print (str(err)) 



 
def type8(nPeople, budget, duration, epochs, genePool, dList, durList, evalFunc, mutationRate, repRate, tags):
    bestSoFar = []
    counter = 0
    eligible = getTaggedDest(genePool, tags)
    population = generateDynamic(eligible, duration, budget, nPeople, 0.75)
    evalFunc(population, budget, nPeople, duration, dList, durList)
    bestSoFar.append(population[0])
    currGen = population
    while counter < repRate and bestSoFar[0][1] < 1.2:
        selected = selection(currGen)
        nextGen = selectionNextGen(eligible, selected, duration, budget, nPeople)
        evalFunc(nextGen, budget, nPeople, duration, dList, durList)
        nextGen.sort(key=takeSecond, reverse=True)
        bestSoFar.append(nextGen[0])
        currGen = nextGen
        counter += 1
    bestSoFar.sort(key=takeSecond, reverse=True)
    return bestSoFar

    
#x = type1(int(nPeople), int(budget), int(duration), epochs, genePool, dList, durList, evaluateV1)
#showResults(x, nPeople, dList, 1, 'type1')
x = type8(int(nPeople), int(budget), int(duration), epochs,genePool,dList,durList, evaluateV1, 0.1,8, TAGS)
showResults(x, nPeople, dList, 1, 'type8', durList)


x = type8(int(nPeople), int(budget), int(duration), epochs,genePool,dList,durList, evaluateV1, 0.1,8, TAGS)
stop = time.process_time()
times=stop-start
showResults(x, nPeople, dList, times, 'type8', durList)

print("Process finished in %f seconds"%times)
print("Result can be found in: newresults.txt")    