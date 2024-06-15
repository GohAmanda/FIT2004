"""
Question:

Implement a directed graph class in Python. Your graph should use an adjacency list representation 
and should support the following operations:
- Initialise the graph with n vertices, where n is a given parameter
- Add a directed, weighted edge between the vertices u and v, with weight w
Focus on making your code easy to use and easy to understand. Avoid using Python lists as obfuscated data 
structures, e.g. please don't store edges like [v1,v2,w]. It is recommended that you make an Edge class to 
store edges for improved readability. Writing e.u, e.v, and e.w is much nicer to read than e[0], e[1], e[2], 
etc, particularly once you start nesting them!

"""
class Graph:
    def __init__(self, argv_vertices_count):
        # array
        self.vertices = [None]*(argv_vertices_count)
        for i in range(argv_vertices_count):
            self.vertices[i] = Vertex(i)

    def __str__(self):
        return_String = ""
        for vertex in self.vertices:
            return_String = return_String + "Vertex " + str(vertex) + "\n"
        return return_String

    def add_edges(self, argv_edges): # add argument if direct = True
       
        for edge in argv_edges:
            u = edge[0]
            v = edge[1]
            w = edge[2]
            #add u to v
            current_edge = Edge(u,v,w)
            current_vertex = self.vertices[u]
            current_vertex.add_edge(current_edge)
            #add v to u (undirected graph)
            #if not direct:
                # current_edge = Edge(v,u,w)
                # current_vertex = self.vertices[v]
                # current_vertex.add_edge(current_edge)

    
    def bfs(self, source): 
        source = self.vertices[source]
        return_bfs =[]
        discovered =[]
        discovered.append(source)
        while len(discovered) > 0:
            u = discovered.pop(0)
            u.visited =True
            return_bfs.append(u)
            for edge in u.edges:
                v= edge.v
                v = self.vertices[v]
                if v.discovered == False:
                    discovered.append(v)
                    v.discovered = True
        return return_bfs

    def dfs(self, source): # Cant run cause didn't add the edges and vertices
        return_dfs =[]
        discovered =[]
        discovered.append(source)
        while len(discovered) > 0:
            u = discovered.pop(0)
            u.visited =True
            return_dfs.append(u)
            for edge in u.edges:
                v = edge.v
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
        self.distance = 0
        self.previous = None

    def __str__(self):
        return_String = str(self.id)
        for edge in self.edges:
            return_String = return_String + "\n with edges" + str(edge)
        return return_String
    
    def add_edge(self, edge):
        self.edges.append(edge)

    def added_to_queue(self):
        self.discovered = True
    
    def visit_node(self):
        self.visited = True
    
    
class Edge:
    def __init__(self, u, v, w):
        self.u = u
        self.v = v
        self.w = w

    def __str__(self):
        return_string = str(self.u) + ", " + str(self.v) + ", " + str(self.w)
        return return_string

# create a graph with 5 vertices
if __name__ == "__main__":
    # vertices
    # vertices ID 0......5
    total_vertices = 6
    my_graph =  Graph(total_vertices)
    #print(my_graph)

    #edges
    edges =[]
    edges.append((3,1,5)) # u=3, v=1, w=5
    edges.append((1,2,1))
    edges.append((3,2,-5))
    edges.append((2,5,-50))

    # what happen if i want a undireced graph
    
    my_graph.add_edges(edges) # add a argument True /False for undirected or directed

    #print(my_graph)

    # run bfs 
    bfs = my_graph.bfs(3)
    for vertex in bfs:
        print(vertex)
