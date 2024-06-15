class Graph:
    def __init__(self, V):
        self.matrix =[None]*len(V)
        for i in range(len(V)):
            self.matrix[i] = [None]*len(V)
       

    def __str__(self):
        return_String = ""
        for vertex in self.matrix:
            return_String =return_String+"Vertex "+str(vertex)+"\n"
        return return_String


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
    def _init_(self, u, v, w):
        self.u = u
        self.v = v
        self.w = w

# create a graph with 5 vertices
if __name__ == "__main__":
    vertices = [0,1,2,3,4]
    my_graph = Graph(V=vertices)
    print(my_graph)