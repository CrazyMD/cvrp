import pandas as pd
import random
import numpy as np
from Node import Node

input_table = pd.read_csv("data.csv", sep=';')
input_table = input_table.drop(columns=["Unnamed: 4"])
# print(input_table.head(5))
# print(input_table.info())

nodes = [Node(node, demand, x, y) for node, demand, x, y in
         zip(input_table['Node'], input_table['Demand'], input_table['x-coordinate'], input_table['y-coordinate'])]


def GASolve(Problem: pd.DataFrame, NoGenerations: int, PopulationSize: int, KeepBest: bool, CrossOverRate: float,
            MutationRate: float) -> float:
    return 0


def createPopulation(nodes: list) -> list:
    population = []
    order_randoms = [random.random() for i in range(len(nodes))]
    vehicle_randoms = [random.randint(1, 9) for i in range(len(nodes))]
    chromosome = [(node, vehicle) for node, vehicle in zip(order_randoms, vehicle_randoms)]
    return chromosome


def calcFitness(chromosome: list) -> float:
    chromosome.sort(key=lambda tup: tup[1])  # sort by vehicle
    randoms = [i[0] for i in chromosome]  # exract randoms from chromosome
    randomsOrder = np.array(
        randoms).argsort().argsort()  # calc list with rank of randoms, e.g. [1,8,2] --> [0,2,3] (zero based index)
    randomsOrder = [i + 1 for i in randomsOrder]  # change to 1 based index
    chromosome = [(random, chromosome[1]) for random, chromosome in zip(randomsOrder, chromosome)]
    maxIndex = max([chrom[1] for chrom in chromosome])  # get number of cars
    vehicles = []
    for i in range(1, maxIndex + 1):  # single lists for vehicles
        vehicle = []
        for each in chromosome:
            if each[1] == i:
                vehicle.append(each[0])
        vehicles.append([i, vehicle])
    print(vehicles)

    for each in vehicles:
        route = each[1]

    return chromosome


pop = createPopulation(nodes)
# print(pop)
print(calcFitness(pop))
