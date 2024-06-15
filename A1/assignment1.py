
class Graph:
    def __init__(self, locations):
        """
            Input: locations

            Time complexity: O(L) where L is the number of locations
            Space complexity: O(L) where L is the number of locations
        """
        self.locations = []
        for location in locations:
            self.locations.append(Vertex(location))
       
    def add_roads(self, roads):
        """
            Function description: 
            The add_roads method will return a list of key locations. u, v, c and d will be passed into 
            the Edge class as parameter and current_edge is pass as a parameter into the Vertex add_roads
            method.

            Input: roads
            Output/Return: list of locations

            Time complexity: O(R) when R is the number of roads 
            Space complexity: O(L+R) where L is the number of locations and R is the number of roads 
        """
        for road in roads:
            u = road[0]
            v = road[1]
            c = road[2] # u to v, travelling alone
            d = road[3] # u to v, travelling 2/more people
           
            current_road = Edge(u,v,c,d)
            current_location = self.locations[u] # current location is set to the position of u in self.locations
            current_location.add_road(current_road) # current road is added into the current_location 
        
        return self.locations
    
    def reset (self):
        """
            Function description: 
            Resets the boolean that is set in the Vertex class

            Time complexity: O(L) where L is the number of locations
            Space complexity: O(1)
        """
        for location in self.locations:
            location.discovered = False
            location.visited = False
            location.previous = None
            

    def dijkstra(self, start, end):

        """
            Function description: 
            Takes in a set of vertices and edges and then calculates the shortest path between the start
            and end location. MinHeap (priority queue) is used to keep track of the locations to be visited, 
            then updates the distance and routes. The weight of the edges changes depending on the number 
            of people travelling. Lastly, the function will return the optimal path which is a list of locations.

            Input: start, end
            Output/Return: optRoute

            Time complexity: O((L+R)log L) where L is the number of locations and R is the number of roads 
            Space complexity: O(L+R) where L is the number of locations and R is the number of roads 
        """
        self.reset() 
        self.passanger = False 
        self.locations[start].time = 0 # set the start location time as 0
        discovered = MinHeap() 

        # insert the time of the start location and the location object associated with the start location
        discovered.insert(self.locations[start].time, self.locations[start]) 

        while discovered.length > 0:
            u = discovered.pop()[1]
            
            if u == self.locations[end]: 
                break
            
            # time complexity for the code below: O(R) where L is the number of locations
            for road in u.roads:
                v = road.v # get the location of v that is connected to u

                if self.passanger == True: 
                    w = road.d # d is the time where location u to v is travelled with passenger (2/more people)
                else:
                    if road.u in passengers:
                        w = road.d 
                        self.passanger = True # set self.passenger as True
                    elif road.u not in passengers:
                        w = road.c # c is the time where location u to v is travelled alone (1 people)

                # time complexity for the code below: 0(log L) where L is the number of locations
                if self.locations[v].discovered == False:  # check if the location is discovered

                    self.locations[v].discovered = True 

                    # time of location v is set as the time of location u plus the time take for travelling from u to v
                    self.locations[v].time = u.time + w 
                    self.locations[v].previous = u 

                    discovered.insert(self.locations[v].time, self.locations[v])
                
                # time complexity for the code below: 0(log L) where L is the number of locations
                elif self.locations[v].visited == False:  # check if the location is visited

                    if self.passanger == True:
                        w = road.d
                    else:
                        if road.u in passengers:
                            w = road.d
                            self.passanger = True
                        elif road.u not in passengers:
                            w = road.c

                    # check if the time of location v is greater than time of location u plus time taken to travel from u to v
                    if self.locations[v].time > u.time + w: 
                        self.locations[v].visited = True  # set the location v to be visited  
                        self.locations[v].time = u.time + w
                        self.locations[v].previous = u
                        discovered.insert(self.locations[v].time, self.locations[v])
                
       
        optRoute = []
        current_location = self.locations[end] # time complexity: 0(L) where L is the number of locations

        if end not in optRoute: # check if the end location is not in the optRoute 
            while current_location != None: 
                optRoute.append(current_location.id)
                current_location = current_location.previous

                if current_location.id == start:
                    optRoute.append(current_location.id)
                    break

        optRoute.reverse() # time complexity: 0(L) where L is the number of locations
        return optRoute # return the optRoute

class Vertex:

    """
        Function description: Used to represent the location in the graph for finding the shortest route.

        Time complexity: O(1)  
        Space complexity: O(1)
    """

    def __init__(self, id):
        """
            Function description: Set multiple attribute such as id, roads, time, discovered, visited and previous
            These attribute will be used to help finding the shortes route.

            Input: id
        """

        self.id = id
        self.roads =[] 
        self.time = float("inf")
        self.discovered = False
        self.visited = False
        self.previous = None
        
    def set_time(self, time):
        """
            Function description: set the values to the repective attribute
            Input: time
        """

        self.time = time
    
    def set_discovered(self):
        """
            Function description: set attribute discovered as True
        """
                
        self.discovered = True

    def set_visited(self):
        """
            Function description: set attribute visited as True
        """
        self.visited = True
    
    def add_road(self, edge):
        """
            Function description: append the edge into the roads attribute
            Input: edge
        """
        self.roads.append(edge)

    def get_road(self):
        """
            Function description: return the roads attribute
        """
        return self.roads
    
    def __lt__(self, id):
        """
            Function description: Compare between 2 Vertex object based on their distance attribute
            Input: id
        """
        return self.distance < id.distance

    def __gt__(self, id): 
        """
            Function description: Compare between 2 Vertex object based on their distance attribute
            Input: id
        """
        return self.distance > id.distance
        
class Edge:
    """
        Function description: Used to represent the roads between two location u and v.

        Time complexity: O(1)  
        Space complexity: O(1) 
    """

    def __init__(self, u, v, c, d):
        """
            Function description: Set multiple attribute such as u, v, c, d
            These attribute will be used to help finding the shortes route.

            Input: u, v, c, d
        """
        self.u = u # location u
        self.v = v # location v
        self.c = c # time if travelling alone (1 people) from u to v
        self.d = d # time if travelling with passengers (2/more people) from u to v

class MinHeap:

    """
        Function description: It has method insert, pop, swap, rise, and sink
       
        Time complexity: O(log L) where L is the number of locations
        Space complexity: O(1)
    """
        
    def __init__(self):
        """
            Function description: 2 attribute is set which is array list and length of the array list
        """
        self.array = [None]
        self.length = 0
    
    def insert(self, time, location): 
        """
            Function description: Insert the time and location into the array list, update the length of 
            array and pass the length as a parameter to the rise method
            
            Input: time, location

            Time complexity: O(log L) where L is the number of location
        """
        self.array.append((time, location))
        self.length +=1
        self.rise(self.length)

    def pop(self):
        """
            Function description: Remove and returns the smallest time, reducing the length of the array, 
            sinks the new root to the proper location.
        
            Time complexity: O(log L) where L is the number of location
        """
        self.swap(1, self.length)
        self.length -=1
        self.sink(1)
        return self.array.pop()
    
    def swap(self,x,y):
        """
            Function description: swap the position of x and y
            
            Input: x, y
        """
        self.array[x], self.array[y] = self.array[y], self.array[x]

    def rise(self, element):
        """
            Function description: Used after inserting an element to move it up min heap until its parent 
            is smaller
        
            Input: element

            Time complexity: O(log L) where L is the number of location
        """
               
        parent = element //2 
        while parent >=1: 
            if self.array[parent] > self.array[element]: 
                self.swap(parent,element)
                element = parent
                parent = element //2
            else:
                break

    def sink(self, element):
        """
            Function description: Used after removing the root element to move the last element 
            to the top of the heap and move it down until both of its children are larger.

            Input: element

            Time complexity: O(log L) where L is the number of location
        """
               
        child = 2*element
        while child <= self.length:
            if child < self.length and self.array[child+1]<self.array[child]:
                child +=1
            if self.array[element] > self.array[child]:
                self.swap(element,child)
                element = child
                child = 2*element
            else:
                break

def optimalRoutes(start, end, passengers, roads):
    """
    Function description: 

    This function will return the shortest time taken path to reach from start location to end location. Calls 
    the Graph's add_roads method and the dijktra method to get the shortest time taken path. When going from 
    start to end there's passengers at different locations. It will depends on the time taken and choose whether 
    to pick up the passenger or not. If the time taken is longer then will not pick up otherwise will pick up.

    Written by Amanda Goh 32694113

    Approach description: 

    L is the number of locations, R is the number of roads

    When the dijktra method is called the start and end parameter is being passed in as parameter. Then 
    it uses MinHeap which has an overall of O(log L) complexity and it is used to keep track of the locations
    to be visited,then updates the distance and routes. It will check whether the length of the min heap 
    is more than 0. If it is more than 0 then the first object is being pop and set as u. Then check if u is 
    the same and the end location if same then break else continue. Next is running a for loop of road in u.roads.
    The time complexity for the following is O(R) as R is the number of roads. In the for loop the v will be set, 
    then the checking of passenger comes in and set the time to be either c or d depends on the number of people
    travelling in total. The location of v will be asked if it is discovered or not. If it is not then it will
    update the time for location v, set the previous location of v to be u and the discovered of location v is set 
    as True. Then time for location v and the location v will be inserted into the min heap. In this case the time 
    complexity is O(log L) the codes are related to the min heap which is O(log L) (insert, discovered, previous, 
    time, visited). After that, there's a checking of whether the location v is visited or not. If it is not
    then the checking of passenger are perform again. Now, it will be checking if there's a shorter time route from 
    u to v.If there is then the time of location v will be updated to the shorter one, the visited location of v 
    is also being set as true, as well as the the previous location of v set as u and lastly it is inserted into 
    the min heap. Lastly it will be taking the optimal route this has a time complexity of O(L). A list called 
    optRoute is creates and the end location is set as current_location. If the end location is not in the optRoute
    then if current_location is not None then the id of the current_location will be added into the optRoute. At last
    the optRoute will be getting and it will be reversed which is a time complexity of O(L) because it is the number
    of locations then optRoute will be return.

    For __lt__ and __gt__ method in the Vertex class I had refered to stack overflow as
    I had a Type error of TypeError: '>' not supported between instances of 'Vertex' and 'Vertex' and hence went
    online to search for solution. 
    A few methods in MinHeap Class I had refered to the course note that was given on Moodle.

    Precondition: The start and the end cannot be the same location
    Postcondition: The path that is shown must be the shortest time taken path

    Input:
        start = 3
        end = 2
        passengers = [0,4,7]
        roads = [(2,3,12,10),(2,6,5,5),
                (3,4,15,12),(3,0,8,7),
                (4,2,10,7),(4,5,18,10),
                (5,6,20,13),(5,4,5,3),
                (6,7,30,15),(7,2,3,1),
                (0,1,10,8),(0,5,10,10),
                (1,2,200,100)]
        
    Output: [3, 0, 5, 4, 2]
        
    Time complexity: 
        Worst: O((|L|+|R|)log L)
    Space complexity: 
        Aux: O(|L|+|R|)
    
    """
    graph = Graph(range(len(roads)+1))
    graph.add_roads(roads) # pass in roads as the parameter into the add_roads method in Graph class
    shortestRoute = graph.dijkstra(start, end) # pass in start and end as parameter into the dijkstra method in Graph class
    return shortestRoute # return the shortest route
    

def select_sections(occupancy_probability):
    """
    Function description: 
    The input occupancy_probability is a 2D array, and it will return the minimum total occupancy that are able
    to be achieved by removing one number from each row. The Dynamic Programming method used is bottom-up.

    Written by Amanda Goh 32694113

    Approach description:
    the length of the input occupancy_probability is being set as n which is actually the number of rows and the
    length of occupancy_probability[0] is being set as m which is the number of columns. 2 2D array is created and
    set as totalOccupancyArr and parent. The following is time complexity of O(n) and space complexity of O(nm) as
    the loop is run for n number of times, the rowOccupancy and rowParent is multiply with m number. Then the
    rowOccupancy and rowParent is append into their respective 2D array. Next is the creation of base case for
    totalOccupancyArr this is a time complexity of O(m) and the space complexity of O(1) .Then the following will be
    a time complexity of O(nm) and space complexity of O(nm). There's nested for loop where the first for loop
    will loop through the range of n starting from 1 then the secon for loop is looping thorugh the range if m.
    In the nested for loop the occupancy_probability at i j is set as the curr sum, then i have if, elif and else.
    First check if j is 0 if it is 0 then it is the first column of the curr_sum row then after checking if it's 0 
    the checking of totalOccupancyArr at i-1, 0  + curr_sum is less than the totalOccupancyArr at i j. If it is lesser
    than the totalOccupancyArr at i j will be updated to the total of totalOccupancyArr at i-1, 0  + curr_sum and the
    parent at i j will be set as 0 as it's from 0. Then in the same condition (j is 0) there will be another checking
    of whether the m is equals to 1, if it is that means there's only 1 column if not it has columns more than 1. This
    means that there's another totalOccupancyArr at i j which are possible to be less than the one at i-1 , 0. So,
    basically if curr_sum has column more than 1 then it will have to check the number above it and the number diagonally
    up left. Then the totalOccupancyArr at i j will be taking the smaller one and the parent at i j will change 
    accordingly. Then for elif it checks if j is m-1 which is the last column, if it is the same concept with the previous 
    one but instead of checking above and diagonally up left it will check above and diagonally up right. 
    Lastly, the else statement checks for columns that is in the middle (not including the first and last column) again it
    is the same concept but this time it is checking diagonally up right, above and diagonally up left. After all are calculated
    there's a variable name min_total_occupancy set as float inf and a start set as None. min_total_occupancy will give the smallest
    total occupancy from the last row of totalOccupancyArr. Then a time complexity: O(m), space complexity: O(1) for the following 
    the for loop running through the range m this loop will go through the last row and all the columns to get the smallest
    total occupancy, once the it is found it will be set as the new min_total_occupancy and start will be set as j which will be used
    for backtracking.Then there is a list of tuple being set as the name sections_location, it includes 2 variable: the index of the 
    last row and the start index. The following code will be time complexity of O(n) and space complexity of O(n) where n is the number 
    of rows. It is O(n) because the for loop run throughs all the rows. This for loop will start with the second last row and it will 
    stop at -1 (because the last row should be of index 0) and it is decrement by 1. j is then set as the parent at i+1, start then the 
    i and j will be added into the sections_location and start will be set as the new j. After the loop the sections_location will be 
    reverse as it was backtracking which is from end to start but we want start to end. Then the min_total_occupancy and
    sections_location will be returned as a list
    
    Precondition: Only one section can be removed from each row, the sections that was chosen must be 
    adjacent vertically or diagonally
    Postcondition: the total occupancy that will be outputted must be the smallest

    Input:
        argv1:
            occupancy_probability = [
                [54,25,93,120,34],
                [11,93,37,41,96],
                [27,19,98,19,76],
                [79,98,70,57,97],
                [94,92,85,55,1],
                [40,81,42,19,86]
            ]
    
    Output: 
        The output will be the minimum total occupancy and a list of n tuples that represents the sections
        that was removed. 
        In this format: [minimum_total_occupancy, sections_location]
        
        [158, [(0, 1), (1, 2), (2, 3), (3, 3), (4, 4), (5, 3)]]
        
    Time complexity: 
        Worst: O(nm) where n is number of rows and m is number of columns
    Space complexity: 
        Aux: O(nm) where n is the number of rows and m is number of columns

    """
    n = len(occupancy_probability) # rows
    m = len(occupancy_probability[0]) # columns 

    # Two 2d array for tracking the parent vertex and the totalMinOccupancy
    totalOccupancyArr = []
    parent = []

    # time complexity: O(n) , space complexity: O(nm)
    for i in range(n):
        rowOccupancy = [float("inf")]*m
        rowParent = [None]*m
        totalOccupancyArr.append(rowOccupancy)
        parent.append(rowParent)

    # time complexity: O(m), space complexity: O(1)
    # the base case of totalOccupancyArr
    for j in range(m):
        totalOccupancyArr[0][j] = occupancy_probability[0][j]

    # time complexity: O(nm), space complexity: O(nm)
    # the recursive case of totalOccupancyArr
    for i in range(1, n):
        for j in range(m):
            # setting the curr_sum as the position (i,j) in the occupancy_probability
            curr_sum = occupancy_probability[i][j] 

            # First column
            if j == 0:

                # calculate the occupancy at i j, adding the first column or second column base on situation
                
                # first column
                if totalOccupancyArr[i-1][0] + curr_sum < totalOccupancyArr[i][j]:
                    totalOccupancyArr[i][j] = totalOccupancyArr[i-1][0] + curr_sum # update the totalOccupancyArr at i j 
                    parent[i][j] = 0 # updating the parent

                #check if the list has second column
                if m != 1: # if column not equals to 1 it means there's one more posibility (diagonally up)
                    #second column
                    if totalOccupancyArr[i-1][1] + curr_sum < totalOccupancyArr[i][j]:
                        totalOccupancyArr[i][j] = totalOccupancyArr[i-1][1] + curr_sum # update the totalOccupancyArr at i j 
                        parent[i][j] = 1 # updating the parent

            # Last column
            elif j == m-1:
                # calculate the occupancy at i j, adding either the second last column or the last column

                # last column
                if totalOccupancyArr[i-1][m-1] + curr_sum < totalOccupancyArr[i][j]:
                    totalOccupancyArr[i][j] = totalOccupancyArr[i-1][m-1] + curr_sum # update the totalOccupancyArr at i j 
                    parent[i][j] = m-1 # updating the parent

                # second last column
                if totalOccupancyArr[i-1][m-2] + curr_sum < totalOccupancyArr[i][j]:
                    totalOccupancyArr[i][j] = totalOccupancyArr[i-1][m-2] + curr_sum # update the totalOccupancyArr at i j 
                    parent[i][j] = m-2 # updating the parent

            # The columns that is not the first and last, it is the ones in between 
            else:
                # calculate the occupancy at i j, adding one of the columns in the middle (not including the first and last column)
                
                # curr_sum plus the occupancy that is positioned at above left of curr_sum (diagonally up to the left)
                if totalOccupancyArr[i-1][j-1] + curr_sum < totalOccupancyArr[i][j]:
                    totalOccupancyArr[i][j] = totalOccupancyArr[i-1][j-1] + curr_sum  # update the totalOccupancyArr at i j 
                    parent[i][j] = j-1 # updating the parent 

                # curr_sum plus the occupancy that is positioned at above of curr_sum 
                if totalOccupancyArr[i-1][j] + curr_sum < totalOccupancyArr[i][j]:
                    totalOccupancyArr[i][j] = totalOccupancyArr[i-1][j] + curr_sum  # update the totalOccupancyArr at i j 
                    parent[i][j] = j # updating the parent

                # curr_sum plus the occupancy that is positioned at above right of curr_sum (diagonally up to the right)
                if totalOccupancyArr[i-1][j+1] + curr_sum < totalOccupancyArr[i][j]:
                    totalOccupancyArr[i][j] = totalOccupancyArr[i-1][j+1] + curr_sum  # update the totalOccupancyArr at i j 
                    parent[i][j] = j+1 # updating the parent
    

    
    # getting the smallest total occupancy
    min_total_occupancy = float('inf') 
    start = None
    
    # time complexity: O(m), space complexity: O(1)
    for j in range(m): 
        # check whether the last row at index j of totalOccupancyArr to be smaller than the min_total_occupancy
        if totalOccupancyArr[n-1][j] < min_total_occupancy:
            # update the value of min_total_occupancy with the smallest total occupancy from the totalOccupancyArr
            min_total_occupancy = totalOccupancyArr[n-1][j] 
            start = j # set the index j as start

    # tuple of 2 variable: n-1(the index of the last row) and start (starting index of a column)
    sections_location = [(n-1, start)]
    
    # time complexity: O(n), space complexity: O(n)
    # the loop start from the second last row(index n-2) and stops at -1 as it should stop at the first row(index 0), decrement by 1
    for i in range(n-2, -1, -1):
        # Taking the value at position (i+1, start) from the 2D array parent and assign it as j
        j = parent[i+1][start] 
        sections_location.append((i, j)) # append the i and j into the sections_locations as a tuple
        start = j

    sections_location.reverse() # time complexity: O(L), space complexity: O(1)
    return [min_total_occupancy, sections_location] # return both the min_total_occupancy and sections_location


if __name__ == "__main__":

    # the start and end location 
    start = 3
    end = 2
    # The locations where there are passengers
    passengers = [0,4,7]
    # The roads that is represented as list of tuple
    roads = [(2,3,12,10),(2,6,5,5),
             (3,4,15,12),(3,0,8,7),
             (4,2,10,7),(4,5,18,10),
             (5,6,20,13),(5,4,5,3),
             (6,7,30,15),(7,2,3,1),
             (0,1,10,8),(0,5,10,2),
             (1,2,200,100)]
    # will get the optimalRoute from start to end
    optRoute = optimalRoutes(start, end, passengers, roads)
    print(optRoute)

    # The occupancy_probability that us represents as a nested list
    occupancy_probability = [
        [54,25,93,120,34],
        [11,93,37,41,96],
        [27,19,98,19,76],
        [79,98,70,57,97],
        [94,92,85,55,1],
        [40,81,42,19,86]
    ]

    # will return the minimum total occupancy and the positions of the sections tooked
    selection = select_sections(occupancy_probability)
    print(selection)

