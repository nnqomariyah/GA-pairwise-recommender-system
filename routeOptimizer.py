from __future__ import print_function
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
from readDistanceMatrix import getDistance
from readDistanceMatrix import getDuration
from readDistanceMatrix import getDistanceList
from math import floor

class RouteOptimizer:

    def __init__(self, data, dList, durList):
        self.chromosome = data[0]
        self.travel_time = data[5]
        self.dList = dList
        self.durList = durList

    def get_distance_data(self, chromosome, distanceList):
        dMatrix = []
        for i in range(len(chromosome.genes)):
            dlist = []
            for j in range(len(chromosome.genes)):
                # print(chromosome.genes[i].name, chromosome.genes[j].name)
                x = getDistance(distanceList, chromosome.genes[i].name, chromosome.genes[j].name)
                if x == -1 or x == 0:
                    dlist.append(15000)
                else:
                    dlist.append(x)
            dMatrix.append(dlist)
        return dMatrix
    
    def create_data_model(self, dMatrix):
        data = {}
        data['distance_matrix'] = dMatrix
        data['num_vehicles'] = 1
        data['depot'] = 0
        return data

    def get_solution(self, manager, routing, solution, chromosome):
        totaldist = solution.ObjectiveValue()
        index = routing.Start(0)
        places_output = ''
        routeList = []
        while not routing.IsEnd(index):
            places_output += ' {} ->'.format(chromosome.genes[index].name)
            routeList.append(index)
            index = solution.Value(routing.NextVar(index))
        daySuggestion = self.day_suggestion(routeList)
        return totaldist, places_output, routeList, daySuggestion

    def day_suggestion(self, routeList):
        days = len(self.chromosome.genes)/3
        # dayHours = ceil(self.chromosome.sumDuration()/days)
        currHour = 0
        plan_day = []
        suggestion = []
        for i in routeList:
            currHour += self.chromosome.genes[i].duration
            if not routeList.index(i) == 0:
                currHour += floor(getDuration(self.durList, self.chromosome.genes[i].name, self.chromosome.genes[routeList.index(i)-1].name)/60/60)
            if currHour <= 10:
                plan_day.append(self.chromosome.genes[i].name)
            else:
                suggestion.append(plan_day)
                plan_day = []
                currHour = self.chromosome.genes[i].duration
                plan_day.append(self.chromosome.genes[i].name)
        suggestion.append(plan_day)
        return(suggestion)


    def get_optimized_route(self):
        dMatrix = self.get_distance_data(self.chromosome, self.dList)
        data = self.create_data_model(dMatrix)
        manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),data['num_vehicles'], data['depot'])
        routing = pywrapcp.RoutingModel(manager)

        def distance_callback(from_index, to_index):
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return data['distance_matrix'][from_node][to_node]

        transit_callback_index = routing.RegisterTransitCallback(distance_callback)

        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = (routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

        solution = routing.SolveWithParameters(search_parameters)

        if solution:
            return self.get_solution(manager, routing, solution, self.chromosome)

