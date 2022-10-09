import random
import numpy as np


class Chromosome:

    def __init__(self, nodes: list):
        self.order_randoms = [random.random() for i in range(len(nodes) - 1)]  # -1 -> do not visit depot
        self.vehicle_randoms = [random.randint(1, 9) for i in range(len(nodes) - 1)]
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
                distance += nodes[node].distances[node + 1]
            if passengers > 100:
                distance += 5000
            vehicle.append(distance)
            vehicle.append(passengers)
            fitness += distance
        return distance
