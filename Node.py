class Node:
    def __init__(self, number, demand, x, y):
        self.number = number
        self.demand = demand
        self.x = x
        self.y = y
        self.distances = []

    def __eq__(self, other):
        return self.number == other

    def __str__(self):
        return str(self.number)

    def __repr__(self):
        return str(self.number)