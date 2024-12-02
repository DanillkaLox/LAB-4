import random
import matplotlib.pyplot as plt
import networkx as nx


class Graph:
    def __init__(self, num_vertices, min_degree, max_degree):
        self.num_vertices = num_vertices
        self.adj_list = {i: set() for i in range(num_vertices)}
        self.generate_random_graph(min_degree, max_degree)

    def generate_random_graph(self, min_degree, max_degree):
        for vertex in range(self.num_vertices):
            degree = random.randint(min_degree, max_degree)
            possible_neighbors = list(set(range(self.num_vertices)) - {vertex} - self.adj_list[vertex])
            while len(self.adj_list[vertex]) < degree and possible_neighbors:
                neighbor = random.choice(possible_neighbors)
                self.adj_list[vertex].add(neighbor)
                self.adj_list[neighbor].add(vertex)
                possible_neighbors.remove(neighbor)

    def get_neighbors(self, vertex):
        return self.adj_list[vertex]


class ABCGraphColoring:
    def __init__(self, graph, num_bees, num_scouts):
        self.graph = graph
        self.num_bees = num_bees
        self.num_scouts = num_scouts
        self.colors = {v: -1 for v in graph.adj_list}
        self.nectar = {v: len(graph.adj_list[v]) for v in graph.adj_list}
        self.history = []
        self.scout_positions = set()

    def get_available_color(self, vertex):
        neighbor_colors = {self.colors[n] for n in self.graph.get_neighbors(vertex) if self.colors[n] != -1}
        for color in range(len(self.graph.adj_list)):
            if color not in neighbor_colors:
                return color

    def color_vertex(self, vertex):
        color = self.get_available_color(vertex)
        self.colors[vertex] = color

    def recolor_neighbors(self, vertex):
        neighbors = self.graph.get_neighbors(vertex)
        for neighbor in neighbors:
            self.colors[neighbor] = -1 
            self.color_vertex(neighbor)

    def run(self, max_iterations, log_interval):
        for iteration in range(1, max_iterations + 1):
            scouts = sorted(self.nectar, key=self.nectar.get, reverse=True)
            active_scouts = 0

            for scout in scouts:
                if self.nectar[scout] > 0 and scout not in self.scout_positions:
                    active_scouts += 1
                    self.scout_positions.add(scout)

                    self.colors[scout] = -1

                    self.recolor_neighbors(scout)

                    self.color_vertex(scout)
                    self.nectar[scout] = 0

                if active_scouts >= self.num_scouts:
                    break

            if iteration % log_interval == 0:
                unique_colors = {self.colors[v] for v in self.colors if self.colors[v] != -1}
                self.history.append((iteration, len(unique_colors)))

            if all(self.nectar[v] == 0 for v in self.graph.adj_list):
                break

    def plot_quality(self):
        iterations, qualities = zip(*self.history)
        plt.figure(figsize=(10, 5))
        plt.plot(iterations, qualities, marker="o")
        plt.xlabel("Iterations")
        plt.ylabel("Number of Colors Used")
        plt.title("Quality of Solution Over Iterations")
        plt.grid(True)
        plt.show()

    def visualize_graph(self):
        G = nx.Graph()
        for vertex, neighbors in self.graph.adj_list.items():
            for neighbor in neighbors:
                G.add_edge(vertex, neighbor)

        color_map = [self.colors[v] for v in G.nodes()]
        plt.figure(figsize=(10, 10))
        nx.draw(G, node_color=color_map, with_labels=True, node_size=500, cmap=plt.cm.tab20)
        plt.title("Graph Coloring Visualization")
        plt.show()


num_vertices = 15
min_degree = 1
max_degree = 5
num_bees = 5
num_scouts = 1
max_iterations = 100
log_interval = 1

graph = Graph(num_vertices, min_degree, max_degree)

abc = ABCGraphColoring(graph, num_bees, num_scouts)
abc.run(max_iterations, log_interval, visualize_each_iteration=True)

abc.visualize_graph()
abc.plot_quality()
