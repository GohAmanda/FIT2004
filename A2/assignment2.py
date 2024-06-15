from collections import deque

# ==================== Q1 Code ====================

def maxThroughput(connectionGraph, maxIn, maxOut, origin, targets):
    """
    This function calculates the maximum throughput in a network
    In this function I have a list that stores the forward and backward edges. 
    I also added a new node called supersink due to having multiple targets.
    For the multiple targets, I added a forward and backward edge from target to supersink or
    supersink to target. Then I call the ford_fulkerson to initialize the max flow

    Written by Amanda Goh Shi Zhen 32694113

    Precondition:
    - origin is not contained in the list targets
    - cannot assume the list of integers targets is in any specific order, but can assume
      no duplicated target
    - cannot assume connection channels are bidirectional

    Postcondition:
    - Will return the maximum throughput in the network

    Input:
        connections: representing communication channels
        maxIn: Maximum incoming flow for each data center
        maxOut: Maximum outgoing flow for each data center
        origin: The source data center
        targets: The target data centers

    Return:
        maxFlow: The maximum throughput in the network

    Time complexity: O(|D| * |C|) where D is the number of data centres and C 
                     is the number of communication channels

    Space complexity: O(|C|) where C is the number of communication channels

    """

    # adjacent list
    original_graph=[]
 
    for i in range(len(maxIn)):
        original_graph.append([])
    
    # Build the adjacent list with the forward and backward edges
    for a, b, t in connectionGraph:
        original_graph[a].append((b,t))
        original_graph[b].append((a,0))

    #Add a supersink (there's multiple target)
    if (len(targets)>0):
        supersink = len(original_graph)
        
    for j in range(1, len(targets)):
        original_graph.append([])
  
    for target in targets:
        # Add the forward edge from target to supersink
        original_graph[target].append((supersink, maxOut[target]))

        # Add the backward ede from supersink to target
        if supersink < len(original_graph):
            original_graph[supersink].append((target, 0)) 
    
    # Initialize the max flow
    maxFlow = ford_fulkerson(original_graph, origin, supersink, maxOut) 
    return maxFlow
    

def ford_fulkerson(original_graph, source, supersink, maxOut):
    """
    This function implements the Ford-Fulkerson algorithm to find the maximum flow in the network.
    This function calls the method in the ResidualNetwork class, the methods that helps to find
    the maximum flow. Runs through the paths getting the capacity using it to count the maximum
    flow then updating the new flow in the residual network.

    Written by Amanda Goh Shi Zhen 32694113

    Precondition:
    - The residual network is constructed with forward and backward edges.
    Postcondition:

    Input:
        original_graph: represents as an adjacency list
        source: The source node in the network
        supersink: The supersink node in the network
        maxOut: Maximum outgoing flow for each data center

    Return:
        maxFlow: The maximum flow in the network

    Time complexity: O(|D| * |C|) where D is the number of data centres and C 
                     is the number of communication channels
                    
    Space complexity: O(1)
    """

    # initialise the maximum flow
    maxFlow = 0 
    
    #initialise the residual network
    residual_network = ResidualNetwork(original_graph)

    # Find the augmenting paths and update the maximum flow as well as 
    # the flow in the networks until no more paths are found
    for path in residual_network.getAugPath(source, supersink):

        # the capacity of the augmenting path
        capacity = residual_network.getCapacity(path,maxOut)

        # update the maximum flow
        maxFlow += capacity

        # Update the flow in the residual network
        residual_network.updateAugFlow(path,capacity)
    return maxFlow

   
class ResidualNetwork():
    def __init__(self,graph):
        """
        This is the constructor method of the ResidualNetwork class

        Written by Amanda Goh Shi Zhen 32694113

        Precondition:
        Postcondition:

        Input:
            graph: The original graph representing the cimmunication network

        Time complexity: O(1)

        Space complexity: O(1)
       
        """
        self.resGraph = graph

    def getAugPath(self, source, sink):
        """
        This function finds all the possible augmenting paths from the source 
        to the supersink in the residual network.

        Written by Amanda Goh Shi Zhen 32694113

        Input:
            source: The source node in the network
            sink: The supersink node in the network

        Return:
            allPaths: A lists of all augmenting paths from the source to 
                      the supersink

        Time complexity: O(|D| + |C|) where D is the number of data centres and C 
                         is the number of communication channels

        Space complexity: O(|D| + |C|) where D is the number of data centres and C 
                         is the number of communication channels

        """
        queue = deque()

        # the list that will be return
        allPaths = []

        queue.append([source,[source]])

        while queue:
            (departs, path) = queue.popleft()
            
            for (arrives, capacity) in self.resGraph[departs]:
               if arrives not in path:
                    # checks if the arrives node is the supersink node
                    if arrives == sink:
                        # if the path reaches the sink
                        # add the supersink into the path
                        path = path + [arrives]

                        #add the path to the list of augmented paths
                        allPaths.append(path)
                    
                    else:
                        # Add the next node to the current path and enqueue it for further exploration
                        queue.append((arrives, path + [arrives]))
                
        return allPaths
        

    def getCapacity(self,path, maxOut):
        """
        This function  calculates the capacity of an augmenting path in the network

        Written by Amanda Goh Shi Zhen 32694113

        Input:
            path: The augmenting path represented as a list of nodes
            maxOut: Maximum outgoing flow for each data center

        Return:
            pathCapacity: The capacity of the augmenting path

        Time complexity: O(|D| * |C|) where D is the number of data centres and C is the number of 
                         communication channels

        Space complexity: O(|D| * |C|) where D is the number of data centres and C is the number of 
                         communication channels
        
        """
        AugPathCapacity = []

        # Iterate over the edges in the path
        for i in range (1,len(path)):
            departs = path[i-1]
            arrives = path[i]
            originalMax = maxOut[departs]
        
            # Find the corresponding edge in the graph
            for j in self.resGraph[departs]:

                if (j[0] == arrives):

                    if j[1] > maxOut[departs]:
                        AugPathCapacity.append(maxOut[departs])

                    if maxOut[departs] == 0:
                        AugPathCapacity.append(0)

                    AugPathCapacity.append(j[1])
                    break
        
        # Determine the minimum capacity along the path
        pathCapacity = min(AugPathCapacity)

        # Update the outflow capacity of the nodes along the path
        for i in range (1,len(path)):
            departs = path[i-1]
            arrives = path[i]
           
            maxOut[departs] -= pathCapacity

            # Special handling for the supersink node
            if (arrives == 5):
                if maxOut[departs] == 0:
                    if len(self.resGraph[departs]) >1: # there's more than one arrives connecting to it
                        maxOut[departs] = originalMax                
        
        return pathCapacity
       
    def updateAugFlow(self, path, pathCapacity):
        """
        This function updates the flow in the residual network along the augmenting path

        Written by Amanda Goh Shi Zhen 32694113

        Input:
            path: The augmenting path represented as a list of nodes
            pathCapacity: The capacity of the augmenting path

        Time complexity: O(C) where C is the number of communication channels

        Space complexity: O(1) 
        """
        for i in range (1,len(path)):
            departs = path[i-1]
            arrives = path[i]

            for j in range(len(self.resGraph[departs])):
                if self.resGraph[departs][j][0] == arrives:
                    # Updating the forward edge
                    newCap = self.resGraph[departs][j][1] - pathCapacity
                    self.resGraph[departs][j] = (arrives, newCap)   

                    # Updating the backward edge
                    if arrives < len(self.resGraph):
                        self.resGraph[arrives].append((departs, 0))
                        
                    break




# ==================== Q2 Code ====================

class Node:
    def __init__(self, size=26):
        """
        Initializes a Node object

        Written by Amanda Goh Shi Zhen 32694113

        Args:
            size: The size of the link array

        Attributes: 
            link: An array to store links to the child nodes
            frequency: The frequency assosiated with the node

        """
        self.link = [None] * size
        self.frequency = 0

class CatsTrie:
    def __init__(self, sentences):
        """
        This constructor initializes the CatsTrie object and builds the trie from 
        the sentences

        Written by Amanda Goh Shi Zhen 32694113

        Input:
            sentences: A list of sentence

        Time complexity: O(N*M) where N is the number of sentences and M is the 
                         number of characters in the longest sentence

        """
        self.root = Node()
        for sentence in sentences:
            self.insert(sentence)

    def insert(self, sentence):
        """
        This function inserts a sentence into the trie

        Written by Amanda Goh Shi Zhen 32694113

        Input:
            sentence: The sentence that will be inserted
            
        Time complexity: O(M) where M is the number of characters of the sentence

        Space complexity: O(M) where M is the number of characters in the longest sentence
        """
        curr = self.root
        self.insert_recur(curr, sentence)

    def insert_recur(self, curr, sentence):
        """
        This is a recursive helper function for inserting a sentence into the trie

        Written by Amanda Goh Shi Zhen 32694113

        Input:
            curr: The current node in the trie
            sentence: the reaming part of the sentence to be inserted

        Time complexity: O(M) where M is the number of characters of the sentence
        """

        # if the length of is 0, means that we have reached the end of the sentence
        if len(sentence) == 0:

            # Increment of the frequency of the current node
            curr.frequency += 1
            return
        
        # if there are still characters remaining in the sentence
        else:
            char = sentence[0]
            index = ord(char) - 97

            # if the link for the current character is None
            # means the node for the current character does not exist
            if curr.link[index] is None:
                # create a new node
                curr.link[index] = Node()
            
            # Recursively move to the next character in the sentence
            self.insert_recur(curr.link[index], sentence[1:])

      
    def autoComplete(self, prompt):
        """
        This function returns the most frequent sentence in the trie that begins 
        with the given prompt

        Written by Amanda Goh Shi Zhen 32694113

        Input:
            prompt: The prompt to be auto complete

        Return:
            sentence: The most frequent sentence that begins with the prompt

        Time complexity: O(X*Y) where X is the length of the prompt and Y is the length 
                         of the most frequent sentence that begins with the prompt
       
        """
        curr = self.root

        # traverse through each character in the prompt
        for char in prompt:

            index = ord(char) - 97

            # if the link for the current character is None, that means there's no sentences 
            # starting with given prompt in the trie 
            if curr.link[index] is None:
                return None
            
            # Move to the next character in the trie by updating the current node
            curr = curr.link[index]
        
        # Once the prompt is traversal through completely, finds the most frequent sentence 
        # starting from the current node
        sentence = self.mostFreqSentence(curr, prompt)

        # returns the most frequence sentence found
        return sentence
    

    def mostFreqSentence(self, curr, char):
        """
        This is a recursive function that finds the most frequence sentence in the trie that
        starts with the given char

        Written by Amanda Goh Shi Zhen 32694113

        Input:
            curr: The current node in the trie
            char: The character of the sentence

        Return:
            The most frequent sentence that starts with the char

        Time complexity: O(X*Y) where X is the length of the prompt and Y is the length 
                         of the most frequent sentence that begins with the prompt
        
        """
        
        # stores the sentence with the highest frequency
        sentence_with_most_freq = None

        # Stores the maximum frequency encountered
        max_freq = 0

        # Update the sentence if the current node has higher frequency
        if curr.frequency > max_freq:
            max_freq = curr.frequency
            sentence_with_most_freq = char

        # Iterate through each link in the current node
        for i in range(len(curr.link)):
            if curr.link[i] is not None:
                current_sentence = self.mostFreqSentence(curr.link[i], char + chr(i + 97))
                current_freq = self.getSentenceFreq(current_sentence)

                # Update the sentence and max frequency if a higher frequency is encountered
                if current_freq > max_freq:
                    max_freq = current_freq
                    sentence_with_most_freq = current_sentence

                # if the frequency is the same, compare the sentences lexicographically and update if it is smaller
                elif current_freq == max_freq and current_sentence < sentence_with_most_freq:
                    max_freq = current_freq
                    sentence_with_most_freq = current_sentence

        # returns the sentence with the highest frequency
        return sentence_with_most_freq
        

    def getSentenceFreq(self, sentence):
        """
        This function returns the frequency of a sentence in the trie

        Written by Amanda Goh Shi Zhen 32694113

        Input:
            sentence: The sentence whose frequency is to be retrieved

        Return:
            freq: The frequency of the sentence

        Time complexity: O(Y) where Y is the length of the most frequent sentence

        Space complexity: O(Y) where Y is the length of the most frequent sentence
        """
        curr = self.root

        # Traverse each character in the sentence
        for char in sentence:
            index = ord(char) - 97

            # Check if the current character's link is None, indicating the sentence is not present in the trie
            if curr.link[index] is None:
                return 0
            
            # Move to the next node in the trie
            curr = curr.link[index]

        # Return the frequency of the sentence found in the trie
        return curr.frequency
    


# ==================== Main Functions ====================

if __name__ == "__main__":
    connections = [(0, 1, 3000), (1, 2, 2000), (1, 3, 1000),(0, 3, 2000), (3, 4, 2000), (3, 2, 1000)]
    maxIn = [5000, 3000, 3000, 3000, 2000]
    maxOut = [5000, 3000, 3000, 2500, 1500]
    origin = 0
    targets = [4,2]
    maxOutput = maxThroughput(connections, maxIn, maxOut, origin, targets)
    print(maxOutput)


    sentences = ["abc", "abazacy", "dbcef", "xzz", "gdbc", "abazacy", "xyz", "abazacy", "dbcef", "xyz", "xxx", "xzz"]
    mycattrie = CatsTrie(sentences)

    prompt = "ab"
    result = mycattrie.autoComplete(prompt)
    print(result)  # Output: abazacy

    prompt = "a"
    result = mycattrie.autoComplete(prompt)
    print(result)  # Output: abazacy

    prompt = "dbcef"
    result = mycattrie.autoComplete(prompt)
    print(result)  # Output: dbcef

    prompt = "dbcefz"
    result = mycattrie.autoComplete(prompt)
    print(result)  # Output: None

    prompt = "ba"
    result = mycattrie.autoComplete(prompt)
    print(result)  # Output: None

    prompt = "x"
    result = mycattrie.autoComplete(prompt)
    print(result)  # Output: xyz

