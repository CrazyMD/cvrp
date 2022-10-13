import random

import pandas as pd
import numpy as np
from Node import Node
from Chromosome import Chromosome

input_table = pd.read_csv("data.csv", sep=';')
input_table = input_table.drop(columns=["Unnamed: 4"])
# print(input_table.head(5))
# print(input_table.info())

nodes = [Node(node, demand, x, y) for node, demand, x, y in
         zip(input_table['Node'], input_table['Demand'], input_table['x-coordinate'], input_table['y-coordinate'])]

for start_node in nodes:  # calc distances between nodes
    for goal_node in nodes:
        start_node.distances.append(
            round(((start_node.x - goal_node.x) ** 2 + (start_node.y - goal_node.y) ** 2) ** 0.5, 5))


def roulette_selection(population: list) -> Chromosome:
    sum_fitness = sum((1 / chrom.fitness) for chrom in population)
    # quotient = [(1 / chrom.fitness) / sum_fitness for chrom in population]
    # index = np.random.choice(range(0, len(population)), p=quotient)  # get index of random choosen element according to roulette selection
    # print(population[index].fitness)
    random_selector = random.random() * sum_fitness
    population.sort(key=lambda x: x.fitness)
    temp_sum = 0
    for each in population:
        temp_sum += (1 / each.fitness)
        if temp_sum > random_selector:
            print(each.fitness)
            return each
    #return population[index]

def recombination(parent1 : Chromosome, parent2 : Chromosome) -> Chromosome
    new_chrom = Chromosome(parent1.node_list) #node_list is same everywhere


population = [Chromosome(nodes) for i in range(0, 100)]
for i in range(0, 100):
    pop_len = len(population)
    new_pop = []
    for j in range(0, pop_len):
        crossover_mutation = random.random()
        if crossover_mutation < 0.5:
            print('')
        else:
            new_pop.append(roulette_selection(population).mutation())

    new_pop.sort(key=lambda x: x.fitness)
    population.sort(key=lambda x: x.fitness)
    population = population[:int(pop_len / 10)]  # keep the best solutions
    population.extend(new_pop[:-int(pop_len / 10)])
population.sort(key=lambda x: x.fitness)
print("best:" + str(population[0].fitness))
print("mean: " + str(sum(chrom.fitness for chrom in population) / len(population)))
print(population[0].vehicle_list)
