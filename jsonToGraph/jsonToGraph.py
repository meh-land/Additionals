import json

class Node:
    def __init__(self, node_id, label):
        self.id = node_id
        self.label = label
        self.adjacent_nodes = []

    def add_adjacent(self, node):
        self.adjacent_nodes.append(node)

    def __repr__(self):
        adjacent_ids = [node.id for node in self.adjacent_nodes]  # Collect only IDs of adjacent nodes
        return f"[id={self.id}, label={self.label}, adjacent_nodes={adjacent_ids}]"


class Graph:
    def __init__(self, json_file):
        self.nodes = []
        self.node_map = {}
        self.read_json(json_file)

    def read_json(self, json_file):
        # Open and read the JSON file
        with open(json_file, 'r') as file:
            data = json.load(file)
            # Load nodes and edges from the JSON data
            self.load_nodes(data['nodes'])
            self.load_edges(data['edges'])

    def load_nodes(self, nodes):
        for node in nodes:
            node_obj = Node(node['id'], node['data']['label'])
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
