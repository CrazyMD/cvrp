from __future__ import annotations
import random
import numpy as np


class Chromosome:

    def __init__(self, nodes: list, parent1: Chromosome, parent2: Chromosome):
        if (parent1 == None and parent2 == None):
            self.order_randoms = [random.random() for i in range(len(nodes) - 1)]  # -1 -> do not visit depot
            self.vehicle_randoms = [random.randint(1, 9) for i in range(len(nodes) - 1)]
            #self.vehicle_randoms = random.sample(list(range(1,9))*7,len(nodes)-1)
            #print(sorted(self.vehicle_randoms))

        elif (parent1 != None and parent2 != None):  # recombination
            if True:
                selection_randoms = [random.random() for i in range(len(nodes) - 1)]
                child = []
                for i in range(len(selection_randoms)):
                    if selection_randoms[i] < 0.5:
                        child.append((parent1.order_randoms[i], parent1.vehicle_randoms[i]))
                    else:
                        child.append((parent2.order_randoms[i], parent2.vehicle_randoms[i]))
                self.order_randoms = [el[0] for el in child]
                self.vehicle_randoms = [el[1] for el in child]
            else:
                crossover_index = random.randint(0, len(parent1.order_randoms))
                self.order_randoms = parent1.order_randoms[:crossover_index] + parent2.order_randoms[crossover_index:]
                self.vehicle_randoms = parent1.vehicle_randoms[:crossover_index] + parent2.vehicle_randoms[crossover_index:]

        elif (parent1 != None and parent2 == None): #mutation (not in-place)
            self.order_randoms = parent1.order_randoms
            self.vehicle_randoms = parent1.vehicle_randoms
            swap_prob = random.random()
            for i in range(0, random.randint(1, 10)):
                swap_index1 = random.randint(0, len(self.order_randoms)-1)
                swap_index2 = random.randint(0, len(self.order_randoms)-1)
                swap_index3 = random.randint(0, len(self.order_randoms) - 1)

                self.order_randoms[swap_index1], self.order_randoms[swap_index2],  self.order_randoms[swap_index3] = self.order_randoms[swap_index3], self.order_randoms[swap_index1], self.order_randoms[swap_index2]

                self.vehicle_randoms[swap_index1], self.vehicle_randoms[swap_index2] = self.vehicle_randoms[swap_index2], \
                                                                                   self.vehicle_randoms[swap_index1]

        self.chromosome_random_code = [(node, vehicle) for node, vehicle in
                                       zip(self.order_randoms, self.vehicle_randoms)]
        self.chromosome_rank_code = self.calc_ranked_code(self.chromosome_random_code)
        self.vehicle_list = self.calc_vehicle_list()
        self.fitness = self.calc_fitness(nodes)

    def calc_ranked_code(self, random_code: list) -> list:
        random_code.sort(key=lambda tup: tup[1])  # sort by vehicle
        randoms = [i[0] for i in random_code]  # extract randoms from chromosome
        randomsOrder = np.array(
            randoms).argsort().argsort()  # calc list with rank of randoms, e.g. [1,8,2] --> [0,2,1] (zero based index)
        # randomsOrder = [i + 1 for i in randomsOrder]  # change to 1 based index
        return [(random, chromosome[1]) for random, chromosome in zip(randomsOrder, random_code)]

    def calc_vehicle_list(self) -> list:
        maxIndex = max([chrom[1] for chrom in self.chromosome_rank_code])  # get number of cars
        vehicles = []
        for i in range(1, maxIndex + 1):  # single lists for vehicles
            vehicle = [0]
            for each in self.chromosome_rank_code:
                if each[1] == i:
                    vehicle.append(each[0])
            vehicle.append(0)
            vehicles.append([i, vehicle])
        return vehicles

    def calc_fitness(self, nodes: list) -> float:
        fitness = 0
        for vehicle in self.vehicle_list:
            distance = 0
            passengers = 0
            for node in vehicle[1]:
                passengers += nodes[node].demand
                distance += nodes[node].distances[vehicle[1][vehicle[1].index(node) + 1]]  # next node in list
            if passengers > 100:
                distance += 5000
            vehicle.append(distance)
            vehicle.append(passengers)
            fitness += distance
        return fitness
