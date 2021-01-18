from chromosome import Chromosome
from readDistanceMatrix import getDistance
from readDistanceMatrix import getDuration
import destination
import random
import csv
import re
import copy
import json
from routeOptimizer import RouteOptimizer

TAXI_RATE = 5000


def readJson(filename):
    jsons = []
    genePool = []
    with open(filename) as f:
        for row in f:
            jsons.append(json.loads(row))
        f.close
    for i in jsons:
        genePool.append(destination.Destination(i["spotName"],re.sub("[^0-9]", "",i["afterPrice"]),i["category"],i["duration"]))
    return genePool

def readJsonV2(filename):
    genePool = []
    with open(filename) as f:
        data = json.loads(f.readline())
        f.close()
    for i in data["places"]:
        genePool.append(destination.Destination(i["name"],i["ticketPrice"],i["types"],i["visitDuration"],i["tags"]))
    return genePool

def findDest(genePool, nameList):
    found = []
    totalHTM = 0
    totalDur = 0
    for i in genePool:
        if i.name in nameList:
            found.append(i)
            totalHTM += i.cost
            totalDur += i.duration
    return found, totalHTM, totalDur/24

def generatePopulation(genePool, duration):
    newPopulation = []
    for i in range(40):
        spots = []
        usedSpots = []
        categories = []
        for i in range(duration*3):
            while True:
                x = random.randint(0,len(genePool)-1)
                if x not in usedSpots:
                    if not(genePool[x].category in categories):
                        break
                    elif genePool[x].category in categories and random.random() > 0.7:
                        break
            spots.append(genePool[x])
            categories.append(genePool[x].category)
            usedSpots.append(x)
        newPopulation.append([Chromosome(spots),0,0,0,0,0])
    return newPopulation

def generateWithTags(genePool, duration):
    newPopulation = []
    for i in range(40):
        spots = []
        usedNums = []
        for i in range(duration*3):
            while True:
                x = random.randint(0,len(genePool)-1)
                if not x in spots:
                    break
            usedNums.append(x)
            spots.append(genePool[x])
        newPopulation.append([Chromosome(spots),0,0,0,0,0])
    return newPopulation

def generateDynamic(genePool, duration, budget, noPeople, costRate):
    budgetThreshold = budget*costRate
    durationTreshold = duration*7
    newPopulation = []
    for i in range(40):
        tDuration = 0
        tBudget = 0
        spots = []
        usedNums = []
        while tDuration < durationTreshold and tBudget < budgetThreshold:
            while True:
                x = random.randint(0,len(genePool)-1)
                if not x in spots:
                    break
            tDuration += genePool[x].duration
            tBudget += genePool[x].cost*noPeople
            usedNums.append(x)
            spots.append(genePool[x])
        newPopulation.append([Chromosome(spots),0,0,0,0,0])
    return newPopulation

def getTaggedDest(genePool, tags):
    eligible = []
    for i in genePool:
        if any(item in i.tags for item in tags):
            eligible.append(i)
    return eligible.copy()

def getFilteredDest(genePool, tags, rspots):
    eligible = []
    for i in genePool:
        if not (i.name in rspots):
            eligible.append(i)
    return eligible.copy()

def selection(population):
    selected = []
    for i in range(40):
        ch1 = population[random.randrange(len(population))]
        while True:
            ch2 = population[random.randrange(len(population))]
            if(ch1 != ch2):
                break
        if ch1[1] > ch2[2]:
            selected.append(ch1.copy())
        else:
            selected.append(ch2.copy())
    return selected

def cross(chromosome1, chromosome2):
    # copy the parents to the child
    ch1 = copy.copy(chromosome1)
    ch2 = copy.copy(chromosome2)

    # generate cross points
    cp1, cp2 = getRandomRange(ch1)
    # print(cp1,cp2)

    # cross phase 1
    selection1 = ch1.genes[cp1:cp2].copy()
    selection2 = ch2.genes[cp1:cp2].copy()
    j = 0
    for i in range(cp1, cp2):
        ch1.genes[i] = selection2[j]
        ch2.genes[i] = selection1[j]
        j += 1
    
    # cross phase 2
    dpCh1 = getDuplicateIndex(ch1.genes)
    dpCh2 = getDuplicateIndex(ch2.genes)
    # print("duplicates -------\n",dpCh1,dpCh2,'\nduplicates -------\n')
    for i in range(len(dpCh1)):
        exchange = random.choice(ch2.genes)
        counter = 0
        while exchange in ch1.genes and counter < 10:
            exchange = random.choice(ch2.genes)
            counter += 1
        ch1.genes[dpCh1[i]] = exchange
    
    for i in range(len(dpCh2)):
        exchange = random.choice(ch1.genes)
        counter = 0
        while exchange in ch2.genes and counter < 10:
            exchange = random.choice(ch1.genes)
            counter += 1
        ch2.genes[dpCh2[i]] = exchange

    return ch1, ch2

def crossv2(genePool, chromosome1, chromosome2, duration, budget, noPerson):
    # prevents random error for 1 day trips
    if len(chromosome1.genes) <= 1 or len(chromosome2.genes) <= 1:
        return chromosome1, chromosome2

    cut1 = random.randint(1, len(chromosome1.genes)-1)
    cut2 = random.randint(1, len(chromosome2.genes)-1)
    
    # crossing
    start1 = chromosome1.genes[:cut1].copy()
    start2 = chromosome2.genes[:cut2].copy()
    end1 = chromosome1.genes[cut1:].copy()
    end2 = chromosome2.genes[cut2:].copy()

    start1.extend(end2)
    start2.extend(end1)

    # cross phase 2
    dpCh1 = getDuplicateIndex(start1)
    dpCh2 = getDuplicateIndex(start2)
    for i in range(len(dpCh1)):
        counter = 0
        exchange = random.choice(genePool)
        while exchange in start1 and counter < 10:
            exchange = random.choice(genePool)
            counter += 1
        start1[dpCh1[i]] = exchange
    
    for i in range(len(dpCh2)):
        exchange = random.choice(genePool)
        counter = 0
        while exchange in start2 and counter < 10:
            exchange = random.choice(genePool)
            counter += 1
        start2[dpCh2[i]] = exchange

    # cross phase 3
    ch1 = cutter(start1, duration, budget, noPerson)
    ch2 = cutter(start2, duration, budget, noPerson)

    return Chromosome(ch1), Chromosome(ch2)

def cutter(spotList, duration, budget, noPerson):
    durationTreshold = duration * 10
    totalDuration = 0
    totalBudget = 0
    cut = []
    for i in spotList:
        totalBudget += i.cost*noPerson
        totalDuration += i.duration
        if totalDuration >= durationTreshold or totalBudget >= budget:
            return cut
        cut.append(i)
    return cut


def mutate(population, genePool, chance):
    for j in range(len(population)):
        if random.random() <= chance:
            chromosome = population[j][0]
            i = random.randint(0,len(chromosome.genes)-1)
            x = genePool[random.randint(0,len(genePool)-1)]
            while x in chromosome.genes:
                x = genePool[random.randint(0,len(genePool)-1)]
            chromosome.genes[i] = x

def getDuplicateIndex(xlist):
    unique = []
    dpIndex = []
    for i in range(len(xlist)):
        if not xlist[i] in unique:
            unique.append(xlist[i])
            # print(unique)
        elif xlist[i] in unique:
            dpIndex.append(i)
            # print(dpIndex)
    return dpIndex

def getRandomRange(chromosome):
    a = random.randrange(len(chromosome.genes))
    b = random.randrange(len(chromosome.genes))
    while a == b:
        b = random.randrange(len(chromosome.genes))
    if a > b:
        return b, a
    else:
        return a, b

# need to evaluate spot's number of people
def evaluateV1(population, budget, noPerson, duration, distanceList, durationList):
    for i in range(len(population)):
        travelExpenses = 0
        travelDuration = 0
        for j in range(len(population[i][0].genes)-1):
            if j <= (len(population[i][0].genes)-1):
                distance = getDistance(distanceList, population[i][0].genes[j].name, population[i][0].genes[j+1].name)
                tDuration = getDuration(durationList, population[i][0].genes[j].name, population[i][0].genes[j+1].name)
                if distance == -1 or distance == 0:
                    # 15000 from average distance of the distance matrix used for testing
                    travelExpenses += 15000
                else:
                    travelExpenses += distance
                if tDuration == -1 or tDuration == 0:
                    # 1300 from average duration (in seconds) from the duration matrix used for testing
                    travelDuration += 1300
                else:
                    travelDuration += tDuration

        travelExpenses = (travelExpenses / 1000) * 5000
        costScore = abs((budget - ((population[i][0].sumCost()*noPerson)+travelExpenses)))/100000
        # print(costScore)
        durationScore = abs((population[i][0].sumDuration() + (travelDuration/60/60)) - (duration*10))
        population[i][1] = 1/(costScore + durationScore)
        # total cost
        population[i][2] = (population[i][0].sumCost()*noPerson)+travelExpenses
        # total duration
        population[i][3] = (population[i][0].sumDuration() + (travelDuration/60/60))
        # travel expenses
        population[i][4] = travelExpenses
        # travel duration
        population[i][5] = (travelDuration/60/60)


# prone to 0 error
def evaluateV2(population, budget, noPerson, duration, distanceList, durationList):
    for i in range(len(population)):
        travelExpenses = 0
        travelDuration = 0
        for j in range(len(population[i][0].genes)-1):
            if j <= (len(population[i][0].genes)-1):
                distance = getDistance(distanceList, population[i][0].genes[j].name, population[i][0].genes[j+1].name)
                tDuration = getDuration(durationList, population[i][0].genes[j].name, population[i][0].genes[j+1].name)
                if distance == -1 or distance == 0:
                    # 15000 from average distance of the distance matrix used for testing
                    travelExpenses += 15000
                else:
                    travelExpenses += distance
                if tDuration == -1 or tDuration == 0:
                    # 1300 from average duration (in seconds) from the duration matrix used for testing
                    travelDuration += 1300
                else:
                    travelDuration += tDuration

        travelExpenses = (travelExpenses / 1000) * 5000
        costScore = abs((budget - ((population[i][0].sumCost()*noPerson)+travelExpenses)))/100000
        # print(costScore)
        durationScore = abs((population[i][0].sumDuration() + (travelDuration/60/60)) - (duration*10))
        population[i][1] = 1/costScore + 1/durationScore

# improvement of V1 with tags
def evaluateV3(population, budget, noPerson, duration, distanceList, durationList, prefTags):
    for i in range(len(population)):
        travelExpenses = 0
        travelDuration = 0
        tagScore = 0
        for j in range(len(population[i][0].genes)-1):
            if j <= (len(population[i][0].genes)-1):
                distance = getDistance(distanceList, population[i][0].genes[j].name, population[i][0].genes[j+1].name)
                tDuration = getDuration(durationList, population[i][0].genes[j].name, population[i][0].genes[j+1].name)
                if distance == -1 or distance == 0:
                    # 15000 from average distance of the distance matrix used for testing
                    travelExpenses += 15000
                else:
                    travelExpenses += distance
                if tDuration == -1 or tDuration == 0:
                    # 1300 from average duration (in seconds) from the duration matrix used for testing
                    travelDuration += 1300
                else:
                    travelDuration += tDuration

        for k in population[i][0].genes:
            check = all(item in k.tags for item in prefTags)
            if check:
                tagScore += 1

        travelExpenses = (travelExpenses / 1000) * 5000
        costScore = abs((budget - ((population[i][0].sumCost()*noPerson)+travelExpenses)))/100000
        durationScore = abs((population[i][0].sumDuration() + (travelDuration/60/60)) - (duration*10))
        population[i][1] = 1/(costScore + durationScore) + (tagScore/len(population[i][0].genes))
        population[i][2] = (population[i][0].sumCost()*noPerson)+travelExpenses
        population[i][3] = (population[i][0].sumDuration() + (travelDuration/60/60))
        population[i][4] = travelExpenses
        population[i][5] = (travelDuration/60/60)
    
def takeSecond(elem):
    return elem[1]

# needs to be improved
def nextGeneration(population):
    nextGen = []
    for i in range(0, len(population), 2):
        x, y = cross(population[i][0], population[i+1][0])
        nextGen.append([x,0,0,0,0,0])
        nextGen.append([y,0,0,0,0,0])
    return nextGen

def selectionNextGen(genePool, population, duration, budget, noPerson):
    nextGen = []
    for i in range(0, len(population), 2):
        x, y = crossv2(genePool, population[i][0], population[i+1][0], duration, budget, noPerson)
        nextGen.append([x,0,0,0,0,0])
        nextGen.append([y,0,0,0,0,0])
    return nextGen

def chanceNextGen(population, chance):
    nextGen = []
    for i in range(0, len(population), 2):
        if(random.random() <= chance):
            x, y = cross(population[i][0], population[i+1][0])
            nextGen.append([x,0,0,0,0,0])
            nextGen.append([y,0,0,0,0,0])
        else:
            nextGen.append([population[i][0],0,0,0,0,0])
            nextGen.append([population[i+1][0],0,0,0,0,0])
    return nextGen

def showResults(results, noPerson, distanceList, time, typename, durationList):
    with open('newresults.txt', 'a') as outfile:
        outfile.write('\n'+typename+'\n')
        avgFitness = 0
        for i in results:
            avgFitness += i[1]

            totaldist, places_output, routeList, daySuggestion = RouteOptimizer(i, distanceList, durationList).get_optimized_route()

            outfile.write(json.dumps({
                "fitness" : i[1],
                "spots" : i[0].getGenes(),
                "HTM" : i[0].sumCost()*noPerson,
                "travelExpenses" : i[4],
                "totalExpenses" : i[2],
                "totalDuration" : i[3],
                "travelDuration" : i[5],
                "totalDist" : totaldist,
                "route" : places_output,
                "route-by-index": routeList,
                "per-day-route": daySuggestion
            })+'\n')
        outfile.write("average fitness:" + str(avgFitness/len(results)))
        outfile.write(" time:" + str(time))
        outfile.close()
        return str(avgFitness/len(results)), str(time)

def runStats(allStats):
    with open('newstats.csv', 'w') as outfile:
        for j in range(len(allStats)):
            outfile.write('type'+str(j+1)+'\navgFitness,Time\n')
            for x in range(len(allStats[j])):
                outfile.write(allStats[j][x][0]+','+allStats[j][x][1]+'\n')

def sendResults(results, noPerson, distanceList, typename, durationList):
    response = {}
    avgFitness = 0
    compNo = 0
    for i in results:
        avgFitness += i[1]

        totaldist, places_output, routeList, daySuggestion = RouteOptimizer(i, distanceList, durationList).get_optimized_route()

        response[str(compNo)] = {
            "fitness" : i[1],
            "spots" : i[0].getGenes(),
            "HTM" : i[0].sumCost()*noPerson,
            "travelExpenses" : i[4],
            "totalExpenses" : i[2],
            "totalDuration" : i[3],
            "travelDuration" : i[5],
            "totalDist" : totaldist,
            "route" : places_output,
            "route-by-index": routeList,
            "per-day-route": daySuggestion
        }
        compNo += 1
    response["average fitness"] = str(avgFitness/len(results))

    return response

def queryResults(results, noPerson, duration, budget, genePool):
    qR = []
    for i in results:
        if ((i[2] - budget)/budget) <= (budget/4):
            if abs(i[3] - duration) >= 2:
                while True:
                    x = genePool[random.randint(0, len(genePool)-1)]
                    if not x in i[0].genes:
                        break
                i[0].genes.append(x)
                qR.append(i)
            else:
                qR.append(i)
    return qR