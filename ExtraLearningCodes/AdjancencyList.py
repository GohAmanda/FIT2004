# Graph class
# This is adjacency list
from multiprocessing.heap import Heap


class Graph:
    def __init__(self, V):
        # array
        self.vertices = [None]*len(V)
        for i in range(len(V)):
            self.vertices[i] = Vertex(V[i])

    def __str__(self):
        return_String = ""
        for vertex in self.vertices:
            return_String =return_String+"Vertex "+str(vertex)+"\n"
        return return_String
    
    def bfs(self, source): # Cant run cause didn't add the edges and vertices
        return_bfs =[]
        discovered =[]
        discovered.append(source)
        while len(discovered)>0:
            u = discovered.pop(0)
            u.visited =True
            return_bfs.append(u)
            for edge in u.edges:
                v= edge.v
                if v.discovered ==False:
                    discovered.append(v)
                    v.discovered = True
        return return_bfs

    def kahn(self): # Cant run cause didn't add the edges and vertices
        self.reset()
        incoming = [0]*len(self.vertices)

        for vertex in self.vertices:
            for edge in vertex.edges:
                incoming[edge.v] = incoming[edge.v] +1
        
        process =[]
        for i in range(len(incoming)):
            if incoming [i] ==0:
                process.append(i)

        while len(process)>0:
            u = process.pop(0)
            u.visited =True
            for edge in u.edges:
                v= edge.v
                v = self.vertices[v]
                if v.discovered ==False and v.visited == False:
                    process.append(v)
                    v.discovered = True
        return "BFS"
    
    def bfs_distance(self, source):
        discovered =[]
        discovered.append(source)
        while len(discovered)>0:
            u=discovered.pop(0)
            u.visited = True
            for edge in u.edges:
                v = edge.v
                if v.discovered ==False:
                    discovered.append(v)
                    v.discovered = u.distance + 1
                    v.previous = u 
    # Implement backtracking on our own

    def dijkstra(self, source, destination):
        source.distance = 0
        discovered = Heap()
        discovered.append(source.distance, source)
        while len(discovered)>0:
            u=discovered.pop(0)
            u.visited = True
            if u == destination:
                return
            for edge in u.edges:
                v = edge.v
                if v.discovered ==False:
                    v.discovered = True # have discovered v, adding into the queue
                    v.discovered = u.distance + edge.w
                    v.previous = u 
                    discovered.append(v.distance, v)
                # it is in heap, but not yet finalize
                elif v.visited == False:
                    # if found a shorter distance, change it
                    if v.distance > u.distance + edge.w:
                        v.distance = u.distance + edge.w #update distance
                        v.previous = u
                        # update heap
                         # Code urself
                        discovered.update(v,v.distance) # update vertex v in heap, with distance v.distance (smaller); perform upheap
                        


    # Implement backtracking on our own


    def dfs(self, source): # Cant run cause didn't add the edges and vertices
        return_dfs =[]
        discovered =[]
        discovered.append(source)
        while len(discovered)>0:
            u = discovered.pop(0)
            u.visited =True
            return_dfs.append(u)
            for edge in u.edges:
                v= edge.v
                if v.discovered ==False:
                    discovered.append(v)
                    v.discovered = True
        return return_dfs
                


class Vertex:
    def __init__(self, id):
        self.id = id
        # list
        self.edges =[]
        self.discovered = False
        self.visited = False

    def __str__(self):
        return_String = str(self.id)
        return return_String
    
    def added_to_queue(self):
        self.discovered = True
    
    def visit_node(self):
        self.visited = True
    

class Edge:
    def __init__(self, u, v, w):
        self.u = u
        self.v = v
        self.w = w

# create a graph with 5 vertices
if __name__ == "__main__":
    vertices = [0,1,2,3,4]
    my_graph = Graph(V=vertices)
    print(my_graph)