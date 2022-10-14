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
            if len(vehicles) >= 9:  # last car
                vehicle.add_node(self.node_list[el])
                if idx == len(self.order_nodes) - 1:  # append after last node is added
                    vehicles.append(vehicle)
                continue
            if (vehicle.passengers + self.node_list[el].demand <= 100) and (vehicle.distance <= 500):
                vehicle.add_node(self.node_list[el])
            else:
                vehicles.append(vehicle)
                vehicle = Vehicle(self.node_list)
                vehicle.add_node(self.node_list[el])
            if idx == len(self.order_nodes) - 1:  # append after last node is added
                vehicles.append(vehicle)
        return vehicles

    def calc_fitness(self) -> float:
        fitness = 0
        for vehicle in self.vehicle_nodes:
            fitness += vehicle.distance
            if vehicle.passengers > 100:
                fitness += 200
        return fitness

    def mutation(self) -> Chromosome:
        method = random.randint(1, 3)
        if method == 1: #swap allel
            new_chrom = Chromosome(self.node_list)
            new_chrom.order_nodes = self.order_nodes
            if self.fitness > 2000:
                max_mut = random.randint(1, 2)
            else:
                max_mut = random.randint(1, 4)
            for i in range(0, max_mut):
                swap_index1 = random.randint(0, len(self.order_nodes) - 1)
                swap_index2 = random.randint(0, len(self.order_nodes) - 1)
                new_chrom.order_nodes[swap_index1], new_chrom.order_nodes[swap_index2] = new_chrom.order_nodes[
                                                                                             swap_index2], \
                                                                                         new_chrom.order_nodes[
                                                                                             swap_index1]
            new_chrom.vehicle_nodes = new_chrom.build_vehicle_order()
            new_chrom.fitness = new_chrom.calc_fitness()
            return new_chrom
        if method == 2: #insert slice on different position
            new_chrom = Chromosome(self.node_list)
            new_chrom.order_nodes = self.order_nodes
            start_idx = random.randint(0, len(new_chrom.order_nodes) - 1)
            if len(new_chrom.order_nodes) - start_idx < 10:
                end_idx = random.randint(start_idx, len(new_chrom.order_nodes) - 1)
            else:
                end_idx = random.randint(start_idx, start_idx + 10)
            slice = new_chrom.order_nodes[start_idx: end_idx]
            del new_chrom.order_nodes[start_idx: end_idx]
            insert_idx = random.randint(0, len(new_chrom.order_nodes) - 1)
            new_chrom.order_nodes[insert_idx:insert_idx] = slice
            new_chrom.vehicle_nodes = new_chrom.build_vehicle_order()
            new_chrom.fitness = new_chrom.calc_fitness()
            return new_chrom
        if method == 3: # swap node on route
            new_chrom = Chromosome(self.node_list)
            new_chrom.order_nodes = self.order_nodes
            new_chrom.vehicle_nodes = new_chrom.build_vehicle_order()
            vehicle_idx = random.randint(0, len(new_chrom.vehicle_nodes) - 1)
            swap_idx1 = random.randint(0, len(new_chrom.vehicle_nodes[vehicle_idx].node_list) - 1)
            swap_idx2 = random.randint(0, len(new_chrom.vehicle_nodes[vehicle_idx].node_list) - 1)
            new_chrom.vehicle_nodes[vehicle_idx].node_list[swap_idx1], new_chrom.vehicle_nodes[vehicle_idx].node_list[
                swap_idx2] = new_chrom.vehicle_nodes[vehicle_idx].node_list[swap_idx2], \
                             new_chrom.vehicle_nodes[vehicle_idx].node_list[swap_idx1]
            new_chrom.fitness = new_chrom.calc_fitness()
            return new_chrom
