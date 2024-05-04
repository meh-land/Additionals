from jsonToGraph import Graph
import os

current_dir = os.path.dirname(os.path.realpath(__file__))
file_path = os.path.join(current_dir, 'new.json')
graph = Graph(file_path)
print(graph.adj_matrix)