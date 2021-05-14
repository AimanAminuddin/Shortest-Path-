from random import randint
import math
import networkx as nx
import matplotlib.pyplot as plt

NODES = 8              # defines number of nodes in the graph
EDGES = 16              # defines number of edges in the graph
DIRECTED = True         # defines if the graph is directed or undirected
NEGATIVE_WEIGHT = False # defines if the edges can have negative weight
INFINITY = math.inf     # defines a variable for infinity


# function that implements the Dijkstra's algorithm for single-pair shortest paths
def change_to_dict(graph):
    my_dict = {}
    length = len(graph)
    for num in range(length):
        
        lst = graph[num]
        my_dict[num] = lst 
        
    return my_dict


def dijkstra(graph,start):
    length = len(graph) 
    victory = change_to_dict(graph)
    vertex_set = [node for node in range(length)]
    distance = [float('inf')] * length
    distance[start] = 0
    cloud = [False] * length

    ## while all the nodes are not in the cloud ## 
    while vertex_set != []:
        # find the vertex that closest to the cloud #
        smallest_distance = float('inf')
        closest_vertex = None
        for vertex in vertex_set:
            if distance[vertex] < smallest_distance:
                smallest_distance = distance[vertex]
                closest_vertex = vertex
                
        # All nodes have distance infinity and no path exist
        # between start to these nodes 
        if closest_vertex == None:
            break

        else:
            # Remove vertex closest to cloud from vertex_set #
            vertex_set.remove(closest_vertex)
            # update cloud to include closest_vertex #
            cloud[closest_vertex] = True

            # update distance of nodes not in clouds if necessary #
            # list of adjacent nodes # 
            adjacent = victory[closest_vertex]

            # Find the next nearest closest_vertex from the cloud #
            if adjacent == []:
                continue
            else:
                for node in adjacent:
                    vertex = node[0]
                    weight = node[1]
                    if not cloud[vertex]:
                        new_distance = distance[closest_vertex] + weight
                        if new_distance < distance[vertex]:
                            distance[vertex] = new_distance
                        else:
                            continue
        
    return distance 
    

    

# function that implements the Floyd-Warshall's algorithm for all-pairs shortest paths
def change_to_dict_of_dict(graph):
    my_dict = {}
    length = len(graph)
    for num in range(length):
        node = graph[num] 
        if node == []:
            my_dict[num] = {}
        else:
            second_dict = {item[0]:item[1] for item in node} 
            my_dict[num] = second_dict 
    
    return my_dict 



def floyd_warshall(graph):
    victory = change_to_dict_of_dict(graph)
    length = len(victory)
    my_dict =  {num:None for num in range(length)}
    for num in range(length):
        my_dict[num] = {num:float('inf') for num in range(length)}
    ## distance from a node to itself is 0 ## 
    for elem in range(length):
        my_dict[elem][elem] = 0 
    
    ## creating an adjacent matrix ## 
    for num in range(length):
        distances = victory[num]
        for dist in distances:
            cost = distances[dist]
            my_dict[num][dist] = cost 
    
    ## Dynamic Programming part ## 
    for k in range(length):
        for i in range(length):
            distance = my_dict[i][k]
            for j in range(length):
                my_dict[i][j] = min(my_dict[i][j],distance+my_dict[k][j])
            
    matrix = []
    for item in my_dict:
        row = []
        for num in range(length):
            row.append(my_dict[item][num])
        matrix.append(row)
            
    return matrix 

    
# function that creates the graph
def make_graph(NUMBER_NODES, NUMBER_EDGES, NEGATIVE_WEIGHT, DIRECTED):
    if NODES*NODES<NUMBER_EDGES: 
        print("Impossible to generate a simple graph with %i nodes and %i edges!\n" %(NUMBER_NODES,NUMBER_EDGES))
        return None
    g = [[] for i in range(NUMBER_NODES)]
    for i in range(NUMBER_EDGES):
        while True:
            start_node = randint(0,NUMBER_NODES-1)
            end_node = randint(0,NUMBER_NODES-1)
            if NEGATIVE_WEIGHT: weight = randint(-20,20)
            else: weight = randint(1,20)
            if (start_node != end_node): 
                found = False
                for j in range(len(g[start_node])): 
                    if g[start_node][j][0] == end_node: found = True
                if not found: break            
        g[start_node].append([end_node, weight])
        if DIRECTED==False: g[end_node].append([start_node, weight])
    return g
 

# function that prints the graph
def print_graph(g, DIRECTED):
    if DIRECTED: G = nx.DiGraph()
    else: G = nx.Graph()
    for i in range(len(g)): G.add_node(i)
    for i in range(len(g)):
        for j in range(len(g[i])): G.add_edge(i,g[i][j][0],weight=g[i][j][1])
    for i in range(len(g)):
        print("from node %02i: " %(i),end="")
        print(g[i])
    try: 
        pos = nx.planar_layout(G)
        nx.draw(G,pos, with_labels=True)
    except nx.NetworkXException:
        print("\nGraph is not planar, using alternative representation")
        pos = nx.spring_layout(G)
        nx.draw(G,pos, with_labels=True)
    if DIRECTED: 
        labels=dict([((u,v,),d['weight']) for u,v,d in G.edges(data=True)])
        nx.draw_networkx_edge_labels(G,pos,edge_labels=labels, label_pos=0.3)
    else:
        labels = nx.get_edge_attributes(G,'weight')
        nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)



    
print("\n\n ******** GENERATING GRAPH ********" )     
g = make_graph(NODES,EDGES,NEGATIVE_WEIGHT,DIRECTED)
if g==None: raise SystemExit(0)
elif NODES<50 and EDGES<2500:
    plt.figure(1,figsize=(10,10))
    print_graph(g,DIRECTED)

print("\n\n ******** PERFORMING DIJKSTRA ********" )    
D = dijkstra(g,0)
print("Single-Pair Distance Table (from node 0): ",end="")
print(D)

print("\n\n ******** PERFORMING FLOYD WARSHALL ********" )   
D = floyd_warshall(g)
print("All-Pairs Distance Table: \n",end="")
for i in range(len(g)): 
    print("from node %02i: " %(i),end="")
    print(D[i])
