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
            # print(each.fitness)
            return each
    # return population[index]


def recombination(parent1: Chromosome, parent2: Chromosome) -> Chromosome:
    new_chrom1 = Chromosome(parent1.node_list)  # node_list is same everywhere
    new_chrom2 = Chromosome(parent1.node_list)
    crossover_index1 = random.randint(0, len(new_chrom1.order_nodes) - 1)
    crossover_index2 = random.randint(0, len(new_chrom1.order_nodes) - 1)
    if crossover_index1 > crossover_index2:
        crossover_index1, crossover_index2 = crossover_index2, crossover_index1

    parent1_slice = parent1.order_nodes[crossover_index1:crossover_index2]
    parent2_slice = parent2.order_nodes[crossover_index1:crossover_index2]
    new_chrom1.order_nodes = parent1.order_nodes[:crossover_index1] + parent2_slice + parent1.order_nodes[
                                                                                      crossover_index2:]
    new_chrom2.order_nodes = parent2.order_nodes[:crossover_index1] + parent1_slice + parent2.order_nodes[
                                                                                      crossover_index2:]
    print(len(new_chrom1.order_nodes))

    chrom1_duplicates = list({el for el in new_chrom1.order_nodes if new_chrom1.order_nodes.count(el) > 1})
    chrom1_duplicates_ind = [i for i, el in enumerate(new_chrom1.order_nodes) if el in chrom1_duplicates]
    print(new_chrom1.order_nodes)
    print(chrom1_duplicates)
    print(chrom1_duplicates_ind)
    chrom2_duplicates = list({el for el in new_chrom2.order_nodes if new_chrom2.order_nodes.count(el) > 1})
    chrom2_duplicates_ind = [i for i, el in enumerate(new_chrom2.order_nodes) if el in chrom2_duplicates]
    chrom1_duplicates_ind = list(filter(lambda el: not((el > crossover_index1) and (el < crossover_index2)),
                                   chrom1_duplicates_ind))
    chrom2_duplicates_ind = list(filter(lambda el: not((el > crossover_index1) and (el < crossover_index2)),
                                   chrom2_duplicates_ind))
    print(chrom1_duplicates_ind)

    for each in chrom1_duplicates_ind:
        print(each)
        new_chrom1.order_nodes[each] = chrom2_duplicates[each]
    for each in chrom2_duplicates_ind:
        new_chrom2.order_nodes[each] = chrom1_duplicates[each]

    new_chrom1.vehicle_nodes = new_chrom1.build_vehicle_order()
    new_chrom1.fitness = new_chrom1.calc_fitness()
    new_chrom2.vehicle_nodes = new_chrom2.build_vehicle_order()
    new_chrom2.fitness = new_chrom2.calc_fitness()
    return new_chrom1


population = [Chromosome(nodes) for i in range(0, 100)]
for i in range(0, 100):
    pop_len = len(population)
    new_pop = []
    for j in range(0, pop_len):
        crossover_mutation = random.random()
        if crossover_mutation < 1:
            new_pop.append(recombination(roulette_selection(population), roulette_selection(population)))
        else:
            new_pop.append(roulette_selection(population).mutation())

    new_pop.sort(key=lambda x: x.fitness)
    population.sort(key=lambda x: x.fitness)
    population = population[:int(pop_len / 10)]  # keep the best solutions
    population.extend(new_pop[:-int(pop_len / 10)])
population.sort(key=lambda x: x.fitness)
print("best:" + str(population[0].fitness))
# print("mean: " + str(sum(chrom.fitness for chrom in population) / len(population)))
print(population[0])
