import pandas as pd
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


def produce_child(parent1 : Chromosome, parent2: Chromosome) -> Chromosome:
    return Chromosome(nodes)

chromosome = Chromosome(nodes)
print(chromosome.chromosome_rank_code)
print(chromosome.vehicle_list)
# print(chromosome.fitness)

population = [Chromosome(nodes) for i in range(0, 10000)]
population.sort(key=lambda x: x.fitness)
print(population[0].fitness)
print(population[1].fitness)
print(population[2].fitness)
print('')