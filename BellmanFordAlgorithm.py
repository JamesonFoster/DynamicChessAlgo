import numpy as np
import time as t 
#==========================================Edge class===========================================
class Edge:
    edges = []
    def __init__(self, start, end, weight):
        self.StartVert = start
        self.EndVert = end
        self.weight = weight
        Edge.edges.append(self)

#==========================================Vertex class===========================================

class Vertex:
    vertices = []
    def __init__(self):
        self.degree = 0
        self.adjVertices = []
        self.adjEdges = []
        Vertex.vertices.append(self)

    #create a directed edge from current vtex to given vtex
    def add_edge(self, endVert, weight):
        E = Edge(self, endVert, weight)
        self.adjEdges.append(E)
        self.adjVertices.append(endVert)
        if endVert == self:
            self.degree += 2
        else:
            self.degree += 1

# ==========================================Graph class===========================================
class Graph:
    def __init__(self, vert, edge):
        self.vertices = vert
        self.edges = edge
        # Initialize a matrix to store adjacency information
        self.adj_Matrix = np.zeros((len(self.vertices), len(self.vertices)))
    def adjMatrix(self):
        N = len(self.vertices)
        self.adj_Matrix = np.zeros((N, N))
        for edge in self.edges:
            i = edge.StartVert.index
            j = edge.EndVert.index
            self.adj_Matrix[i][j] = edge.weight
        return self.adj_Matrix
    # Bellman-Ford Algorithm Implementation
    def bellman_ford(self, source):
        dist = {vertex: float('inf') for vertex in self.vertices}
        predecessors = {vertex: None for vertex in self.vertices}
        dist[source] = 0

        # This is the core of the algorithm, where shortest paths are found.
        V = len(self.vertices) 
        for i in range(V - 1):
            relaxed = False 
            for e in self.edges: # Iterate through all edges
                u, v, w = e.StartVert, e.EndVert, e.weight
                
                # Relaxation Check: A path to v through u is shorter than the current path to v
                if dist[u] != float('inf') and dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    predecessors[v] = u
                    relaxed = True
            
            # Optimization: If no distances were updated in a full pass, we can stop early.
            if not relaxed:
                break
                
        # If still able to relax any edge, a negative cycle is reachable from the source.
        for e in self.edges:
            u, v, w = e.StartVert, e.EndVert, e.weight
            
            # If the relaxation condition holds one last time, a negative cycle exists.
            if dist[u] != float('inf') and dist[u] + w < dist[v]:
                print("\nGraph contains a negative cycle accessible from the source.")
                return (True, dist, predecessors) 
        
        # Return result if no negative cycle is found
        print("\nBellman-Ford completed successfully (no negative cycles detected).")
        return (False, dist, predecessors)
    
    def get_road(self, predecessors, start, end, vertex_to_name):
        path = []
        current = end
        while current != None:
            path.insert(0, vertex_to_name.get(current, str(current)))
            if current == start:
                break
            current = predecessors.get(current) 
        # If the path starts with the end but not the start, it means 'end' is unreachable
        if not path or path[0] != vertex_to_name.get(start, str(start)):
             return "Unreachable"
             
        return " -> ".join(path)

# ==========================================Example Usage===========================================
start = t.time() 
i1 = Vertex()
i2 = Vertex()
i3 = Vertex()
i4 = Vertex()
it = Vertex()

# Create a map for object to name for readable output
vertex_to_name = {i1: 'i1', i2: 'i2', i3: 'i3', i4: 'i4', it: 'it'}
def get_vertex_name(vertex_obj):
    return vertex_to_name.get(vertex_obj, 'UnknownVertex')

# Create edges between vertices with weights
i4.add_edge(i1, 0.0833)
i1.add_edge(i2, 0.1)
i1.add_edge(i4, 1)
i1.add_edge(i3, 0.1333)
i3.add_edge(it, 0.31)

g = Graph(Vertex.vertices, Edge.edges)

# Run Bellman-Ford algorithm from source vertex A
print("\nRunning Bellman-Ford Algorithm with i4 as the source")
negative_cycle, distances, predecessors = g.bellman_ford(i4)

# Print results
if not negative_cycle:
    sorted_vertices = sorted(g.vertices, key=lambda v: get_vertex_name(v))

    for vertex in sorted_vertices:
        name = get_vertex_name(vertex)
        distance = distances[vertex]
        
        if distance != float('inf'):
            path = g.get_road(predecessors, i4, vertex, vertex_to_name)
            print(f"Shortest path of edge: {name}. Distance: {distance:.1f}. Path: {path}")
        else:
            print(f"There is no path from i4 to {name}. Distance: Infinity")
else:
    print("Negative weight cycle found. Shortest paths cannot be determined.")
end = t.time()
print(f"Time: {end - start:.6f} seconds\n")
