# Ivan Vigliante
# CS2302 TR 10:20am-11:50am
# Lab 6
# Professor Aguirre, Diego
# TA Saha Manoj
# Date of last modification: 12/04/2018
# The purpose of this program is to test the Graph class and
# the kruskal minimum spanning tree and topological sort algorithms.
from timeit import default_timer as timer
from Graph import GraphAL

#   ___1__
#  /   |   \
# 0----3----2---4
#

print("TEST 1:")
start = timer()
try:
    # Test algorithms with acyclic, undirected graph
    graph_a = GraphAL(5,False)
    graph_a.add_edge(0,1,2)
    graph_a.add_edge(1,2,5)
    graph_a.add_edge(2,3,1)
    graph_a.add_edge(4,2,3)
    graph_a.add_edge(1,3,5)
    graph_a.add_edge(0,3,7)
    print("Kruskal's algorithm MST:")
    edges = graph_a.kruskal_mst()
    for edge in edges:
        print("Edge", edge[0], "-", edge[1], "Weight:",edge[2])
    print(graph_a.topological_sort())
except Exception as ee:
    print(ee)
print("Runtime:", round((timer()-start)*1000,4), "milliseconds.")

#  0<----3----->1<-----2
print("\nTEST 2:")
start = timer()
try:
    # Test algorithms with acyclic, directed graph
    graph_b = GraphAL(4,True)
    graph_b.add_edge(3,0,7)
    graph_b.add_edge(3,1,10)
    graph_b.add_edge(2,1,2)
    vertices = graph_b.topological_sort()
    print("Topological sort order:",vertices)
    graph_b.kruskal_mst()
except Exception as ee:
    print(ee)
print("Runtime:", round((timer()-start)*1000,4), "milliseconds.")

#          _____>2____>
#         /            \
#  0---->1<-------------3
print("\nTEST 3:")
start = timer()
try:
    # Test algorithms with cyclic, directed graph
    graph_b = GraphAL(4,True)
    graph_b.add_edge(0,1,2)
    graph_b.add_edge(1,2,3)
    graph_b.add_edge(2,3,6)
    graph_b.add_edge(3,1,7)
    vertices = graph_b.topological_sort()
    print("Topological sort order:",vertices)
    graph_b.kruskal_mst()
except Exception as ee:
    print(ee)
print("Runtime:", round((timer()-start)*1000,4), "milliseconds.")