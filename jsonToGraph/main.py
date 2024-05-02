#!/bin/python3
from jsonToGraph import Graph

graph = Graph(r'new.json')
print(graph.get_adjacency_list())
