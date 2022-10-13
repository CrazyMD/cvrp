from __future__ import annotations

from Node import Node


class Vehicle:

    def __init__(self, nodes: list):
        self.nodes = []
        self.passengers = 0
        self.distance = 0
        self.node_list = nodes  # complete node list

    def add_node(self, node: Node):
        self.nodes.append(node)
        self.passengers += node.demand
        self.calc_distance()

    def calc_distance(self):
        route = [self.node_list[0]]
        route.extend(self.nodes)
        route.append(self.node_list[0])
        dist = 0
        for i in range(0,len(route)-1):
            # if idx == len(route):
            # break
            dist += self.node_list[route[i].number].distances[route[i+1].number]
        self.distance = dist

    def __str__(self):
        return str(self.nodes)

    def __repr__(self):
        return str([self.nodes,self.distance,self.passengers])