#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
@author: jwhite

@email: josh@securemind.org

@description: This is script demonstrates the construction of a simple network multigraph 
and utilizes Dijkstra's shortest path algorithm from the networkx library to find an print 
all simple paths. In addition it demonstrates path decision calculations using IGRP metric.
You can alter the default values for k1, k2, k3 if you want as well as the static latency 
per km. 

In this example, weight is equivilent to distance in km and capacity is measure in gigabits 
per second.  
'''

##################################################
##################################################
###      This section defines the imports      ###
##################################################
##################################################

import networkx as nx
import pylab
import matplotlib.pyplot as plt

startnode = "a" # define the start node for the path diagram
endnode = "c" # define the end node for the path diagram

pathquestion = ["a", "b", "c", "d"] # Enter any path of nodes and the system will check and see if the link is possible given existing edges.

latencyperkm = 3.34 # Static variable for SMF28 Fiber

##################################################
##################################################
###  This section defines the main functions   ###
##################################################
##################################################

def define_network():
    ''' This function defines the network nodes, edges between nodes (network links) and there locations on the output plot '''
    G.add_node("a",color='purple', pos=(1,1))
    G.add_node("b",color='purple', pos=(1,2))
    G.add_node("c",color='purple', pos=(2,2))
    G.add_node("d",color='purple', pos=(2,1))  
    
    G.add_node("i",color='lightblue', pos=(3,1.5))
        
    G.add_node("e",color='orange', pos=(4,1))
    G.add_node("f",color='orange', pos=(4,2))
    G.add_node("g",color='orange', pos=(5,2))
    G.add_node("h",color='orange', pos=(5,1))  
    
    '''
    edge variables: 
          weight = distance in k
          capacity in Gbps
          latency in milliseconds (we're using a constant from: 
                                   http://www.m2optics.com/blog/bid/70587/Calculating-Optical-Fiber-Latency
                                   of: 3.34 microsecond per kilometer
          usage in %
    '''
    G.add_edge("a", "b", color='blue', weight=10, capacity=15, latency=(10 * 3.34), usage=.50)   
    G.add_edge("b", "c", color='blue', weight=10, capacity=10, latency=(10 * 3.34), usage=.50)  
    G.add_edge("b", "d", color='blue', weight=20, capacity=12, latency=(20 * 3.34), usage=.50)  
    G.add_edge("d", "c", color='blue', weight=10, capacity=30, latency=(10 * 3.34), usage=.50)
    
    G.add_edge("d", "i", color='blue', weight=30, capacity=15, latency=(30 * 3.34), usage=.50)
    G.add_edge("e", "i", color='blue', weight=30, capacity=10, latency=(30 * 3.34), usage=.50)

    G.add_edge("e", "f", color='blue', weight=10, capacity=40, latency=(10 * 3.34), usage=.50)   
    G.add_edge("f", "g", color='blue', weight=10, capacity=80, latency=(10 * 3.34), usage=.50)  
    G.add_edge("e", "g", color='blue', weight=20, capacity=20, latency=(20 * 3.34), usage=.50)  
    G.add_edge("h", "g", color='blue', weight=10, capacity=20, latency=(10 * 3.34), usage=.50)

def make_reference_graph_plot():
    ''' This function defines the initial network plot based on the define_network function '''
    define_network()
    
    pos=nx.get_node_attributes(G,'pos')
    colors = nx.get_node_attributes(G, 'color')
    colors = list(colors.values())
    labels = {(n1,n2): ' '.join([str(G[n1][n2]['weight']), "km"]) for (n1,n2) in G.edges()}
    edgecolors = nx.get_edge_attributes(G, 'color')
    edgecolors = list(edgecolors.values())
    
    pylab.figure(1, figsize=(8, 4))
    nx.draw_networkx(G,pos, with_labels=True, node_color=colors, edge_color=edgecolors, linewidths=10, width=3)
    nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)
    
    plt.grid(b=True, color='#d3d3d3')
    plt.show()
    return pos

#######################################################
#######################################################
### DRAW THE SHORTEST PATH AS A SEPERATE GRAPH      ###
### AND COLOR THE NODES AND EDGES BASED ON THE PATH ###
#######################################################
#######################################################

def node_colors(G, path):
    ''' This function colors the nodes on the graph based on their role in the shortest path '''
    colors = []
    for node in G.nodes():
        if node in path:
            colors.append('g')
        else:
            colors.append('purple')
    return colors

def edge_colors(G, path):
    ''' This function colors the edges on the graph based on their role in the shortest path '''
    pcolors = []
    for edge in G.edges():
        if edge in path:
            pcolors.append('g')
        else:
            pcolors.append('b')
    return pcolors

def get_path_pairs(path):
    ''' This function gets the node pairs that make up the edges in the shortest path '''
    shortest_path_list = []
    for x, y in zip(path, path[1:]): 
        pair = x, y
        shortest_path_list.append(pair) 
    return shortest_path_list

def draw_shortest_path(G, pos, start, end):
    ''' This function draws the plot of the shortest path seperate from the initial plot '''
    path = nx.shortest_path(G, start, end, weight='weight')
    print("\nThe shortest path is:", path)
    colors = node_colors(G, path)
    pathpairs = get_path_pairs(path)
    print("\nThe shortest path represented as pairs is:", pathpairs)
    pathweightarray = []
    for x1, x2 in pathpairs:
        pathweightarray.append(G[x1][x2]["weight"])
        
    print("\nThe total path length is:", " ".join([str(sum(pathweightarray)), "Kilometers"]))
    pcolors = edge_colors(G, pathpairs)
    edge_labels = {(n1,n2): ' '.join([str(G[n1][n2]['weight']), "km"]) for (n1,n2) in G.edges()}
    pylab.figure(1, figsize=(8, 4))
    nx.draw_networkx(G, pos, node_color=colors, edge_color=pcolors, linewidths=10, width=3)
    nx.draw_networkx_edge_labels(G , pos, edge_labels=edge_labels)
    plt.grid(b=True, color='#d3d3d3')
    pylab.show()
    
def print_all_simple_paths(G, startnode, endnode):
    ''' This function returns all possible paths from the startnode to the end node as a list of lists '''
    for paths in nx.all_simple_paths(G, startnode, endnode):    
        print(paths)

##################################################
##################################################
###   THESE FUNCTIONS REFER TO LINK CAPACITY   ###
##################################################
##################################################

def get_path_capacity(G, start, end):
    ''' This function returns a list of the link capacities for each link in the shortest path '''
    linkcapacity = []
    path = nx.shortest_path(G, start, end, weight='weight')
    pathpairs = get_path_pairs(path)
    for x1,x2 in pathpairs:
        linkcap = x1, x2, ' '.join([str(G[x1][x2]["capacity"]), "Gbps"])
        linkcapacity.append(linkcap)
    return linkcapacity

def bottle_neck_link_capacity(G, start, end):
    ''' This function returns the link that will cause the first link capacity bottleneck in the shortest path'''
    linkcapacity = get_path_capacity(G, startnode, endnode)
    biggest = 0
    bottleneckfound = ("a","b") # something to default to if nothing is found
    for item in linkcapacity:
        start, end, capacity = item
        capacity = int(capacity.strip("Gbps"))
        if capacity >= biggest:
            biggest = capacity
        else:
            bottleneckfound = item
    return bottleneckfound

def draw_capacity_bottleneck(G, pos, start, end, bottleneckfound):
    ''' This function plots the link that will be the first bottleneck in the path '''
    path = nx.shortest_path(G, start, end, weight='weight')
    pathpairs = get_path_pairs(path)
    colors = node_colors(G, path)
    pcolors = []
    for edge in G.edges():
        if edge in pathpairs:
            if edge == bottleneckfound[0:2]:
                pcolors.append('r')
            else:
                pcolors.append('g')
        else:
            pcolors.append('b')
    
    edge_labels = {(n1,n2): ' '.join([str(G[n1][n2]['capacity']), "Gbps"]) for (n1,n2) in G.edges()}
    
    pylab.figure(1, figsize=(8, 4))
    nx.draw_networkx(G, pos, node_color=colors, edge_color=pcolors, linewidths=10, width=3)
    nx.draw_networkx_edge_labels(G , pos, edge_labels=edge_labels)
    plt.grid(b=True, color='#d3d3d3')
    pylab.show()

##################################################
##################################################
###       Other Path Analysis Functions        ###
##################################################
##################################################

def is_path_valid(g, pathquestion):
    ''' This function checks to see if a user questions path is valid or not '''
    plen = len(pathquestion)
    for i in range(plen - 1):
        if not G.has_edge(pathquestion[i], pathquestion[i + 1]):
            return False
    return True

##################################################
##################################################
###       Routing Calculation Functions        ###
##################################################
##################################################

def igrp_routing_calculation(G, pos, start, end):
    ''' This function calculates the best path based on igrp given an input of graph and stard/end nodes
        it uses the all simple paths function to find all possible routes and then calcuates each routes
        metric given an igrp metric of available bandwidth (kbps) * delay (microseconds/10) 
        Metric = [K1 * Bandwidth + (K2 * Bandwidth)/(256-load) + K3*Delay] 
        where K1, K2, K3 are 1, 0, and 1 by default, load defaults to 1 '''
        
    path = nx.shortest_path(G, start, end, weight='weight')
    pathpairs = get_path_pairs(path)
    
    k1 = 1
    k2 = 0
    k3 = 1
    load = 1
    
    paths_metrics_array = []
    
    for paths in  nx.all_simple_paths(G, start, end):
        delay_array = []
        bandwidth_compare = 100000000000000000 # some huge number to start with
        pathpairs = get_path_pairs(paths)
        
        for pair in pathpairs:
            x1, x2 = pair
            
            bandwidth_calc = (G[x1][x2]["capacity"] * G[x1][x2]["usage"]) * 1000000
            #print(bandwidth_calc)
            if bandwidth_calc <= bandwidth_compare:
                bandwidth_compare = bandwidth_calc
            else:
                bandwidth_calc = bandwidth_calc
            
            delay_calc = G[x1][x2]["latency"] / 10
            #print(G[x1][x2]["latency"])
            delay_array.append(delay_calc)
            
        igrp_metric = ((k1 * bandwidth_compare) + ((k2 * bandwidth_compare) / (256 - load)) + (k3 * sum(delay_array)))
        paths_metrics_array.append([paths, igrp_metric])

        #print(paths)
        #print(igrp_metric)  
    return paths_metrics_array

def lowest_path_metric(igrp_path_metrics):
    ''' This function takes the previous IGRP path metrics and finds the lowest one '''

    default_metric = 1000000000
    for metric in igrp_path_metrics:
        if metric[1] <= default_metric:
            default_metric = metric[1]
    
    for item in igrp_path_metrics:

        if default_metric in item:
            path_default = item

    return default_metric, path_default

##################################################
##################################################
###      THIS IS WHERE THE MAGIC BEGINS        ###
##################################################
##################################################

print("\nGenerating the initial network plot")
G = nx.Graph()
pos = make_reference_graph_plot() # call the first plot and when it's done return the possitions

print("You selected node:", startnode, "to start the path analysis and node:", endnode, "to end the path analysis")

print("\nGenerate the shortest path graph")
draw_shortest_path(G, pos, startnode, endnode)

print("\nThe following is a list of all possible paths from node:", startnode, "to node:", endnode)  
print_all_simple_paths(G, startnode, endnode)

linkcapacity = get_path_capacity(G, startnode, endnode)
print("\nThe capacity of each pair within the shortest path is:", linkcapacity)

bottleneckfound = bottle_neck_link_capacity(G, startnode, endnode)
print("\nThe link between:", bottleneckfound, "will cause bottlenecking due to it's capacity being smaller than the agregate bandwidth")
# Print the plot of the first bottleneck (iteration is backwards from the path list)
draw_capacity_bottleneck(G, pos, startnode, endnode, bottleneckfound)

print("\nThe path:", pathquestion, "that is being question is possible:", is_path_valid(G, pathquestion))

igrp_path_metrics = igrp_routing_calculation(G, pos, startnode, endnode)
print("\nFor each simple path found from start node to end node, the following IGRP metrics were calculated:", igrp_path_metrics)

igrp_path_metric, igrp_default_path = lowest_path_metric(igrp_path_metrics)
print("\nThe path that will be chossen by default if IGRP is used as a routing protocol is:", igrp_default_path[0], "with a metric of:", igrp_path_metric)