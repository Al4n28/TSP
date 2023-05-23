import random
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict

class Graph:
    def __init__(self, num_nodes, edge_percentage, max_weight,same_weight_prob):
        self.graph = nx.DiGraph()
        self.generate_random_graph(num_nodes, edge_percentage, max_weight,same_weight_prob)
        
    def get_graph(self):
        return self.graph
    
    def prim_algorithm(self, adjacency_list, num_nodes):
        visited = [False] * num_nodes
        start_node = random.randint(0, num_nodes - 1)
        visited[start_node] = True
        num_edges = 0
        mst_edges = []

        while num_edges < num_nodes - 1:
            min_weight = float('inf')
            min_edge = None

            for node in range(num_nodes):
                if visited[node]:
                    for neighbor, weight in adjacency_list[node]:
                        if not visited[neighbor] and weight < min_weight:
                            min_weight = weight
                            min_edge = (node, neighbor)

            if min_edge:
                u, v = min_edge
                mst_edges.append((u, v))
                visited[v] = True
                num_edges += 1
            else:
                break

        return mst_edges
    
    def add_edge_with_weights(self, source_node, target_node, same_weight_prob, max_weight):
        if random.random() <= same_weight_prob:
            weight = random.randint(1, max_weight)
            self.graph.add_edge(source_node, target_node, weight=weight)
            self.graph.add_edge(target_node, source_node, weight=weight)
        else:
            weight_source_target = random.randint(1, max_weight)
            weight_target_source = random.randint(1, max_weight)
            self.graph.add_edge(source_node, target_node, weight=weight_source_target)
            self.graph.add_edge(target_node, source_node, weight=weight_target_source)

    def generate_random_graph(self, num_nodes, edge_percentage, max_weight,same_weight_prob):
        self.graph.add_nodes_from(range(num_nodes))

        # Generate all possible edges
        all_edges = [(i, j) for i in range(num_nodes) for j in range(num_nodes) if i != j]

        if edge_percentage == 0:
            adjacency_list = defaultdict(list)
            # Generate random weights for each pair of nodes
            for i in range(num_nodes):
                for j in range(i + 1, num_nodes):
                    weight = random.randint(1, max_weight)
                    adjacency_list[i].append((j, weight))
                    adjacency_list[j].append((i, weight))
            # Use Prim's algorithm to build a minimum spanning tree
            mst_edges = self.prim_algorithm(adjacency_list, num_nodes)
            for source_node, target_node in mst_edges:
                self.add_edge_with_weights(source_node, target_node, same_weight_prob, max_weight)


        elif edge_percentage == 1:
            # Add all possible edges
            for source_node, target_node in all_edges:
                self.add_edge_with_weights(source_node, target_node, same_weight_prob, max_weight)

        else:
            # Calculate the number of edges to retain based on the edge percentage
            num_edges = len(all_edges)
            num_edges_to_retain = int(num_edges * edge_percentage)

            # Randomly select edges to retain
            selected_edges = random.sample(all_edges, num_edges_to_retain)

            # Generate the edges in the graph
            for source_node, target_node in selected_edges:
                self.add_edge_with_weights(source_node, target_node, same_weight_prob, max_weight)
        
    def print_graph_data(self):
        # Number of nodes
        num_nodes = self.graph.number_of_nodes()
        print("Number of nodes:", num_nodes)

        # Edge percentage
        total_possible_edges = num_nodes * (num_nodes - 1)
        edge_percentage = self.graph.number_of_edges() / total_possible_edges
        print("Edge percentage:", edge_percentage)

        print("Number of Edges:", self.graph.number_of_edges())
        
        # Adjacency list
        adj_list = [(u, v, attrs["weight"]) for u, v, attrs in self.graph.edges(data=True)]
        print("Adjacency list:")
        print("[" + ", ".join([f"({u}, {v}, Weight: {weight})" for u, v, weight in adj_list]) + "]")

    def draw_graph(self):
        plt.figure(figsize=(8, 6))
        pos = nx.spring_layout(self.graph)
        nx.draw(self.graph, pos, with_labels=True)

        edge_labels = {}
        for u, v, d in self.graph.edges(data=True):
            if d["weight"] == self.graph.get_edge_data(v, u)["weight"]:
                edge_labels[(u, v)] = f'({d["weight"]})'
            else:
                edge_labels[(u, v)] = f'{u} -> {v} ({d["weight"]})\n{v} --> {u} ({self.graph.get_edge_data(v, u)["weight"]})'
        
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels)
        #[nx.draw_networkx_edge_labels(G,pos,edge_labels={e:i},font_color=cmap[i]) for i,e in enumerate(G.edges())]
        plt.title("Random Graph")
        plt.axis("off")
        plt.show()
        
    def print_adjacency_list_by_node(self):
        print("Adjacency list by node:")
        for node in self.graph.nodes():
            adj_list = [(v, attrs["weight"]) for _, v, attrs in self.graph.out_edges(node, data=True)]
            adj_list_str = " ".join([f"(to {v}, weight {weight})" for v, weight in adj_list])
            print(f"Node {node}: {adj_list_str}")