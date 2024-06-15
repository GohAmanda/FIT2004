"""
Q7:
Recall from lectures that breadth-first search can be used to find single-source shortest paths 
on unweighted graphs, or equivalently, graphs where all edges have weight one. Consider the similar 
problem where instead of only having weight one, edges are now allowed to have weight 0/1. We call
this the zero-one shortest path problem. Write psuedocode for an algorithm for solving this problem. 
Your solution should run in O(V+E) time (this means that you can not use Dijkstra's algorithm!) [Hint:
Combine ideas from breath-first search and Dijkstra's algorithm]

Priotize 0 first 

Ways to do 

(1)
have queue for 0 n have a queue for 1
queue1 = all the 0's
queue2 = all the 1's

or

(2)
have a dequeue when 0 prepend if 1 append 
--> means 0 will go to the front and 1 will be go to the end

or

(3)
Dijkstra
"""

