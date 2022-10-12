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
    random_selector = random.random() * (sum_fitness)
    # population.sort(key=lambda x: x.fitness)
    temp_sum = 0
    for each in population:
        temp_sum += each.fitness
        if (temp_sum > random_selector):
            print(each.fitness)
            return each
    # return population[index]


population = [Chromosome(nodes, None, None) for i in range(0, 50)]
for i in range(0, 1000):
    pop_len = len(population)
    new_pop = []
    for j in range(0, pop_len):
        crossover_mutation = random.random()
        if crossover_mutation < 0.3:
            parent1 = roulette_selection(population)
            parent2 = roulette_selection(population)
            new_pop.append(Chromosome(nodes, parent1, parent2))
        else:
            new_pop.append(Chromosome(nodes, roulette_selection(population), None))
        # population.sort(key=lambda x: x.fitness)
    # population = population[:500]
    population.sort(key=lambda x: x.fitness)
    best_chrom = population[0]
    population = new_pop
    population[random.randint(0, len(population) - 1)] = best_chrom
    population.sort(key=lambda x: x.fitness)
    print("best:" + str(population[0].fitness))
    print("mean: " + str(sum(chrom.fitness for chrom in population) / len(population)))

# population = [Chromosome(nodes) for i in range(0, 10000)]
population.sort(key=lambda x: x.fitness)
print(population[0].fitness)
print(population[0].vehicle_list)
# print(population[1].fitness)
# print(population[2].fitness)

# parent1 = Chromosome(nodes, None, None)
# parent2 = Chromosome(nodes, None, None)
# child = Chromosome(nodes, parent1, parent2)
# print(parent1.vehicle_list)
# print(parent2.vehicle_list)
# print(child.vehicle_list)
