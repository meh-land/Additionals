import json
import numpy as np
import os

class Node:
    def __init__(self, node_id, label, X, Y):
        self.id = node_id
        self.label = label
        self.X = X
        self.Y = Y
        self.pose = np.array([X, Y])
        self.adjacent_nodes = []

    def add_adjacent(self, node):
        self.adjacent_nodes.append(node)

    def __repr__(self):
        adjacent_ids = [node.id for node in self.adjacent_nodes]  # Collect only IDs of adjacent nodes
        return f"id={self.id}, label={self.label}, position=({self.pose}), adjacent_nodes={adjacent_ids}"


class Graph:
    def __init__(self, json_file):
        self.nodes = []
        self.node_map = {}
        self.map_name = ""
        self.read_json(json_file)
        self.N = len(self.nodes)
        self.adj_matrix = np.identity(self.N)
        self.cost_matrix = np.full((self.N, self.N), np.inf)
        self.populate_adj_mat()
        self.populate_cost_mat()

        # Save adjacency matrix to file
        adj_mat_filename = os.getenv("MATRIX_DIR") + self.map_name + ".adj"
        np.savetxt(adj_mat_filename, self.adj_matrix)
        
        # Save cost matrix to file
        cost_mat_filename = os.getenv("MATRIX_DIR") + self.map_name + ".cost"
        np.savetxt(cost_mat_filename, self.cost_matrix)


    def __repr__(self) -> str:
        representation = ""
        for n in self.nodes:
            representation += n.__repr__() + "\n"
        return representation

    def read_json(self, json_file):
        # Open and read the JSON file
        with open(json_file, 'r') as file:
            data = json.load(file)
            self.map_name = data['name']
            # Load nodes and edges from the JSON data
            self.load_nodes(data['nodes'])
            self.load_edges(data['edges'])

    def load_nodes(self, nodes):
        for node in nodes:
            node_obj = Node(node['id'], node['data']['label'], node['data']['X'], node['data']['Y'])
            self.nodes.append(node_obj)
            self.node_map[node['id']] = node_obj

    def load_edges(self, edges):
        # Add each edge to the graph by updating the adjacency list
        for edge in edges:
            source = self.node_map.get(edge['source'])
            target = self.node_map.get(edge['target'])
            # Ensure both nodes are already in the graph; add the connection in both directions
            if source and target:
                source.add_adjacent(target)
                target.add_adjacent(source)

    def get_nodes(self):
        # Return Nodes object (Array of Nodes)
        return self.nodes
    
    def populate_adj_mat(self):
        # Loop over all starting nodes
        for n in range(self.N):
            curr_node = self.nodes[n]
            # Loop to populate adj matrix
            for i in range(self.N):
                if self.nodes[i] in curr_node.adjacent_nodes:
                    self.adj_matrix[n, i] = 1

    def populate_cost_mat(self):
        # Loop over all starting nodes
        for i in range(self.N):
            for j in range(self.N):
                n1 = self.nodes[i]
                n2 = self.nodes[j]
                # If there is a path between n1 and n2
                if n2 in n1.adjacent_nodes:
                    # Put the cost of moving from n1 to n2 as the distance between them
                    self.cost_matrix[i,j] = np.linalg.norm(n1.pose - n2.pose)

        np.fill_diagonal(self.cost_matrix, 0)


