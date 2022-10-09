class Node:
    def __init__(self, number, demand, x, y):
        self.number = number
        self.demand = demand
        self.x = x
        self.y = y
        self.distances = []

    def __eq__(self, other):
        return self.number == other
