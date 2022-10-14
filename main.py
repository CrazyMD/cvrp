import random
import pandas as pd
import numpy as np
from Node import Node
from Chromosome import Chromosome

input_table = pd.read_csv("data.csv", sep=';')
input_table = input_table.drop(columns=["Unnamed: 4"])

nodes = [Node(node, demand, x, y) for node, demand, x, y in
         zip(input_table['Node'], input_table['Demand'], input_table['x-coordinate'], input_table['y-coordinate'])]

for start_node in nodes:  # calc distances between nodes
    for goal_node in nodes:
        start_node.distances.append(
            round(((start_node.x - goal_node.x) ** 2 + (start_node.y - goal_node.y) ** 2) ** 0.5, 5))


def roulette_selection(population: list) -> Chromosome:
    selection = 1
    if selection == 1:  # roulette
        sum_fitness = sum((1 / chrom.fitness) for chrom in population)
        random_selector = random.random() * (sum_fitness)
        population.sort(key=lambda x: x.fitness)
        temp_sum = 0
        for each in population:
            if each.fitness < 1400:
                return each
            temp_sum += (1 / each.fitness)
            if temp_sum > random_selector:
                return each
    if selection == 2:  # tournament
        el_list = []
        for i in range(0, 10):
            el_list.append(population[random.randint(0, len(population) - 1)])
        el_list.sort(key=lambda x: x.fitness)
        return el_list[0]
    if selection == 3: #random
        return population[random.randint(0, len(population) - 1)]


def recombination(parent1: Chromosome, parent2: Chromosome) -> Chromosome:
    new_chrom1 = Chromosome(parent1.node_list)  # node_list is same everywhere
    new_chrom2 = Chromosome(parent1.node_list)
    crossover_index1 = random.randint(0, int((len(new_chrom1.order_nodes) - 1) / 4))
    crossover_index2 = random.randint(0, int((len(new_chrom1.order_nodes) - 1) / 4))
    if crossover_index1 > crossover_index2:
        crossover_index1, crossover_index2 = crossover_index2, crossover_index1

    parent1_slice = parent1.order_nodes[crossover_index1:crossover_index2]
    parent2_slice = parent2.order_nodes[crossover_index1:crossover_index2]
    new_chrom1.order_nodes = parent1.order_nodes[:crossover_index1] + parent2_slice + parent1.order_nodes[
                                                                                      crossover_index2:]
    new_chrom2.order_nodes = parent2.order_nodes[:crossover_index1] + parent1_slice + parent2.order_nodes[
                                                                                      crossover_index2:]
    # print(len(new_chrom1.order_nodes))

    chrom1_duplicates = list({el for el in new_chrom1.order_nodes if new_chrom1.order_nodes.count(el) > 1})
    chrom1_duplicates_ind = [i for i, el in enumerate(new_chrom1.order_nodes) if el in chrom1_duplicates]
    # print(new_chrom1.order_nodes)
    # print(chrom1_duplicates)
    # print(chrom1_duplicates_ind)
    chrom2_duplicates = list({el for el in new_chrom2.order_nodes if new_chrom2.order_nodes.count(el) > 1})
    chrom2_duplicates_ind = [i for i, el in enumerate(new_chrom2.order_nodes) if el in chrom2_duplicates]
    chrom1_duplicates_ind = list(filter(lambda el: not ((el >= crossover_index1) and (el < crossover_index2)),
                                        chrom1_duplicates_ind))
    chrom2_duplicates_ind = list(filter(lambda el: not ((el >= crossover_index1) and (el < crossover_index2)),
                                        chrom2_duplicates_ind))
    # print(chrom1_duplicates_ind)

    for idx, each in enumerate(chrom1_duplicates_ind):
        new_chrom1.order_nodes[each] = chrom2_duplicates[idx]
    for idx, each in enumerate(chrom2_duplicates_ind):
        new_chrom2.order_nodes[each] = chrom1_duplicates[idx]

    new_chrom1.vehicle_nodes = new_chrom1.build_vehicle_order()
    new_chrom1.fitness = new_chrom1.calc_fitness()
    new_chrom2.vehicle_nodes = new_chrom2.build_vehicle_order()
    new_chrom2.fitness = new_chrom2.calc_fitness()
    return new_chrom1


population = [Chromosome(nodes) for i in range(0, 50)]
for i in range(0, 800):
    pop_len = len(population)
    new_pop = []
    for j in range(0, pop_len):
        crossover_mutation = random.random()
        if crossover_mutation < 0.5:
            new_pop.append(recombination(roulette_selection(population), roulette_selection(population)))
        else:
            new_pop.append(roulette_selection(population).mutation())
    #population = list(new_pop)  # try for not keeping the best solutions
    population.sort(key=lambda x: x.fitness)
    population = population[:int(pop_len / 50)]  # keep the best solutions
    population.extend(new_pop[:-int(pop_len / 50)])

    population.sort(key=lambda x: x.fitness)
    print("best:" + str(population[0].fitness))
    print(population[0].vehicle_nodes)
population.sort(key=lambda x: x.fitness)
print("best:" + str(population[0].fitness))
# print("mean: " + str(sum(chrom.fitness for chrom in population) / len(population)))
print(population[0])
