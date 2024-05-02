import json

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
            node_data = {
                'id': node['id'],
                'label': node['data']['label'],
                'adjacent_nodes': []
            }
            self.nodes.append(node_data)
            self.node_map[node['id']] = node_data

    def load_edges(self, edges):
        # Add each edge to the graph by updating the adjacency list
        for edge in edges:
            source_id = edge['source']
            target_id = edge['target']
            source_node = self.node_map.get(source_id)
            target_node = self.node_map.get(target_id)
            # Ensure both nodes are already in the graph; add the connection in both directions
            if source_node and target_node:
                source_node['adjacent_nodes'].append({'node': target_id, 'label': target_node['label']})
                target_node['adjacent_nodes'].append({'node': source_id, 'label': source_node['label']})

    def get_nodes(self):
        # Return Nodes object (Array of Nodes)
        return self.nodes