import json

class Graph:
    def __init__(self, json_file):
        self.graph = {}
        self.read_json(json_file)
        
    def read_json(self, json_file):
        # Open and read the JSON file
        with open(json_file, 'r') as file:
            data = json.load(file)
            # Load nodes and edges from the JSON data
            self.load_nodes(data['nodes'])
            self.load_edges(data['edges'])
    
    def load_nodes(self, nodes):
        # Initialize graph dictionary with each node id as a key and an empty list for connections
        for node in nodes:
            node_id = node['id']
            if node_id not in self.graph:
                self.graph[node_id] = []

    def load_edges(self, edges):
        # Add each edge to the graph by updating the adjacency list
        for edge in edges:
            source = edge['source']
            target = edge['target']
            # Ensure both nodes are already in the graph; add the connection in both directions
            if source in self.graph and target in self.graph:
                self.graph[source].append(target)
                self.graph[target].append(source)  # Add this line to make connections bidirectional

    def get_adjacency_list(self):
        # Return the adjacency list representation of the graph
        return self.graph