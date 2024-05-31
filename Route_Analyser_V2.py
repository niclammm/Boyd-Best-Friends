import gspread
import os
import heapq
from collections import defaultdict
import time

sa = gspread.service_account(filename='service_account.json')   
sh = sa.open("Boyd_Best_Friends")

wks = sh.worksheet("Sheet1")

wks.get_all_values()

class Graph:
    def __init__(self):
        self.vertices = set()
        self.edges = defaultdict(list)
        self.weights = {}

    def add_edge(self, u, v, weight):
        self.vertices.add(u)
        self.vertices.add(v)
        self.edges[u].append((v, weight))
        self.edges[v].append((u, weight))
        self.weights[(u, v)] = weight
        self.weights[(v, u)] = weight

    def prim_minimum_spanning_tree(self):
        mst = []
        visited = set()
        start_vertex = next(iter(self.vertices))
        visited.add(start_vertex)
        heap = [(weight, start_vertex, neighbor) for neighbor, weight in self.edges[start_vertex]]
        heapq.heapify(heap)

        while heap:
            weight, u, v = heapq.heappop(heap)
            if v not in visited:
                visited.add(v)
                mst.append((u, v, weight))
                for neighbor, weight in self.edges[v]:
                    if neighbor not in visited:
                        heapq.heappush(heap, (weight, v, neighbor))

        return mst

    def dijkstra(self, start):
        distances = {vertex: float('infinity') for vertex in self.vertices}
        distances[start] = 0
        priority_queue = [(0, start)]

        while priority_queue:
            current_distance, current_vertex = heapq.heappop(priority_queue)

            if current_distance > distances[current_vertex]:
                continue

            for neighbor, weight in self.edges[current_vertex]:
                distance = current_distance + weight

                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(priority_queue, (distance, neighbor))

        return distances

    def find_odd_degree_vertices(self):
        return [vertex for vertex in self.vertices if len(self.edges[vertex]) % 2 != 0]

    def hierholzer_eulerian_circuit(self, start_vertex):
        def dfs(u):
            while graph[u]:
                v, _ = graph[u].pop(0)
                dfs(v)
            circuit.append(u)

        graph = defaultdict(list)
        for u in self.edges:
            for v, weight in self.edges[u]:
                graph[u].append((v, weight))

        circuit = []
        dfs(start_vertex)
        circuit.reverse()

        return circuit

    def print_coordinates(self, circuit, coordinates):
        row = 1 
        for vertex in circuit:
            coord_x, coord_y = coordinates[vertex]
            print(f"Coordinate: {vertex}, Coordinates: ({coord_x}, {coord_y})")

        for vertex in circuit:
            coord_x, coord_y = coordinates[vertex]
            wks.update_cell(row, 1, vertex)
            wks.update_cell(row, 2, coord_x)
            wks.update_cell(row, 3, coord_y)
            row += 1

def read_input_file(file_name):
    coordinates = {}
    edges = []
    with open(file_name, 'r') as file:
        reading_coordinates = True
        for line in file:
            line = line.strip()
            if not line:
                reading_coordinates = False
                continue
            if reading_coordinates:
                name, x, y = line.split(',')
                coordinates[name.strip()] = (float(x.strip()), float(y.strip()))
            else:
                start, end, weight = line.split(',')
                edges.append((start.strip(), end.strip(), float(weight.strip())))
    return coordinates, edges

if __name__ == "__main__":
    graph = Graph()

    # Print current working directory to debug the file path issue
    print("Current working directory:", os.getcwd())

    # Read coordinates and edges from a file
    file_name = input("Enter the name of the input file: ")
    coordinates, edges = read_input_file(file_name)

    # Add nodes to the graph and capture the first node
    first_node = None
    for name in coordinates:
        graph.vertices.add(name)
        if first_node is None:
            first_node = name  # Capture the first node

    # Add edges to the graph
    for start, end, weight in edges:
        graph.add_edge(start, end, weight)

    mst_edges = graph.prim_minimum_spanning_tree()
    mst_graph = Graph()
    for u, v, weight in mst_edges:
        mst_graph.add_edge(u, v, weight)

    # Find odd degree vertices in the MST
    odd_degree_vertices = mst_graph.find_odd_degree_vertices()

    # Adding a counter to avoid infinite loops
    loop_counter = 0
    max_loops = 100  # This is arbitrary; adjust as necessary for your data

    while len(odd_degree_vertices) > 0 and loop_counter < max_loops:
        u = odd_degree_vertices.pop()
        shortest_distances = graph.dijkstra(u)
        min_distance = float('infinity')
        closest_vertex = None

        for v in odd_degree_vertices:
            if shortest_distances[v] < min_distance and (u, v) in graph.weights:
                min_distance = shortest_distances[v]
                closest_vertex = v

        if closest_vertex and (u, closest_vertex) in graph.weights:
            mst_graph.add_edge(u, closest_vertex, graph.weights[(u, closest_vertex)])
            print(f"Added edge between {u} and {closest_vertex}")
        else:
            print(f"Edge between {u} and {closest_vertex} does not exist in the original graph or has already been added")
        
        odd_degree_vertices = mst_graph.find_odd_degree_vertices()
        loop_counter += 1

    if loop_counter == max_loops:
        print("Reached maximum loop count, possible infinite loop detected.")

    eulerian_circuit = mst_graph.hierholzer_eulerian_circuit(first_node)
    mst_graph.print_coordinates(eulerian_circuit, coordinates)

