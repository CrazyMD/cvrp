from __future__ import annotations
import random
import numpy as np
from Vehicle import Vehicle


class Chromosome:

    def __init__(self, nodes: list):
        self.node_list = nodes
        self.order_nodes = self.build_permutation()
        self.vehicle_nodes = self.build_vehicle_order()
        self.fitness = self.calc_fitness()

    def build_permutation(self) -> list:
        return list(np.random.permutation(range(1, len(self.node_list))))

    def build_vehicle_order(self) -> list:
        vehicles = []
        vehicle = Vehicle(self.node_list)
        for idx, el in enumerate(self.order_nodes):
            if len(vehicles) >= 9:  #last car
                vehicle.add_node(self.node_list[el])
                if idx == len(self.order_nodes)-1: # append after last node is added
                    vehicles.append(vehicle)
                continue
            if (vehicle.passengers + self.node_list[el].demand <= 100) and (vehicle.distance <= 500):
                vehicle.add_node(self.node_list[el])
            else:
                vehicles.append(vehicle)
                vehicle = Vehicle(self.node_list)
                vehicle.add_node(self.node_list[el])
            if idx == len(self.order_nodes)-1:  # append after last node is added
                vehicles.append(vehicle)
        return vehicles

    def calc_fitness(self) -> float:
        fitness = 0
        for vehicle in self.vehicle_nodes:
            fitness+= vehicle.distance
            if vehicle.passengers>100:
                fitness+=500
        return fitness

    def mutation(self) -> Chromosome:
        new_chrom = Chromosome(self.node_list)
        new_chrom.order_nodes=self.order_nodes
        swap_index1 = random.randint(0, len(self.order_nodes) - 1)
        swap_index2 = random.randint(0, len(self.order_nodes) - 1)
        new_chrom.order_nodes[swap_index1], new_chrom.order_nodes[swap_index2] = new_chrom.order_nodes[swap_index2], new_chrom.order_nodes[swap_index1]
        new_chrom.vehicle_nodes = new_chrom.build_vehicle_order()
        new_chrom.fitness = new_chrom.calc_fitness()
        return new_chrom