
import numpy as np
import math
import time

#==========================================Edge class===========================================
class Edge:
    edges = []
    def __init__(self, start, end, weight):
        self.StartVert = start
        self.EndVert = end
        self.weight = weight
        self.name = start.name + end.name

        Edge.edges.append(self)
        start.adjEdges.add(self)
        end.adjEdges.add(self)

#==========================================Vertex class===========================================

class Vertex:
    vertices = []
    def __init__(self, name):
        self.degree = 0
        self.adjVertices = []
        self.adjEdges = set()
        self.name = name
        Vertex.vertices.append(self)

#==========================================Graph class===========================================

#takes a list of vertices and list of edges 
class Graph:
    def __init__(self, vert, edge):
        self.vertices = vert
        self.edges = edge
        
        self.N = len(self.vertices)
        self.E = len(self.edges)
        self.adjMx = np.zeros(shape = (self.N, self.N))

    #creates an edge from start vtex to end vtex
    #takes two vertex objects and an number for weight
    def add_edge(self, startVert, endVert, weight):
        E = Edge(startVert, endVert, weight)
        s = self.vertices.index(startVert)
        d = self.vertices.index(endVert)
        self.adjMx[d][s] = E.weight
        self.adjMx[s][d] = E.weight
        
    def dijkstra(self, start, end):

        start_vertex = self.vertices.index(start)
        end_vertex = self.vertices.index(end)
        distances = [math.inf] * self.N
        predecessors = [None] * self.N
        distances[start_vertex] = 0
        visited = [False] * self.N
    
        for _ in range(self.N):
            min_distance = math.inf
            u = None
            for i in range(self.N):
                if not visited[i] and distances[i] < min_distance:
                    min_distance = distances[i]
                    u = i
            
            #u is the index of the shortest unvisited vertex in the list of vertices
            if u is None:
                break

            visited[u] = True

            for v in range(self.N):
                if self.adjMx[u][v] != 0 and not visited[v]: #if u connected to v and v not visited
                    alt = distances[u] + self.adjMx[u][v] #calculate the alternate distance to the current
                    if alt < distances[v]: #update to the new distance if the current is longer
                        distances[v] = alt
                        predecessors[v] = u #update the predecessor of v to be u
        
        return distances[end_vertex], self.get_path(predecessors, self.vertices[start_vertex], self.vertices[end_vertex])
    
    def get_path(self, predecessors, start_vertex, end_vertex):
        path = []
        edgePath = []
        current = self.vertices.index(end_vertex)
        while current is not None:
            v = self.vertices[current]
            for e in v.adjEdges:
                #if the current vertex has an edge from it to its predecessor, then add it to the path
                if (e.EndVert == self.vertices[predecessors[current]] 
                    or e.StartVert == self.vertices[predecessors[current]]) and e.weight == self.adjMx[current][predecessors[current]]:
                    edgePath.insert(0, e)

            current = predecessors[current] #update current to be the predecessor of current
            if current == self.vertices.index(start_vertex):
                break

        return edgePath  
    
#==========================================Main Function===========================================

def __main__():
    u = Vertex('u')
    v = Vertex('v')
    x = Vertex('x')
    y = Vertex('y')
    w = Vertex('w')
    z = Vertex('z')
    G1 = Graph(Vertex.vertices, Edge.edges)
    
    G1.add_edge(u, v, 7)
    G1.add_edge(u, x, 5)
    G1.add_edge(u, w, 3)
    G1.add_edge(v, w, 3)
    G1.add_edge(v, y, 4)
    G1.add_edge(w, x, 4)
    G1.add_edge(y, z, 2)
    G1.add_edge(y, x, 7)
    G1.add_edge(z, x, 9)
    G1.add_edge(w, y, 8)
    
    print(G1.adjMx)

    starttime = time.time()
    distances, path = G1.dijkstra(u, z)
    endtime = time.time()
       
    print(distances)
    
    for e in path:
        print(e.name)

    runtime = endtime - starttime
    print(f'Runtime: {runtime:.4f}')

if __name__ == "__main__":
    __main__()

#heavily borrowed algorithm code from w3schools' dijkstra's algorithm, modified to output edge list and to work with my classes
