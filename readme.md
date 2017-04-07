NAME
    network-plotting-examples - @author: jwhite

DESCRIPTION
    @email: josh@securemind.org
    
    @description: This is script demonstrates the construction of a simple network multigraph 
    and utilizes Dijkstra's shortest path algorithm from the networkx library to find an print 
    all simple paths. In addition it demonstrates path decision calculations using IGRP metric.
    You can alter the default values for k1, k2, k3 if you want as well as the static latency 
    per km. 
    
    In this example, weight is equivilent to distance in km and capacity is measure in gigabits 
    per second.

FUNCTIONS
    bottle_neck_link_capacity(G, start, end)
        This function returns the link that will cause the first link capacity bottleneck in the shortest path
    
    define_network()
        This function defines the network nodes, edges between nodes (network links) and there locations on the output plot
    
    draw_capacity_bottleneck(G, pos, start, end, bottleneckfound)
        This function plots the link that will be the first bottleneck in the path
    
    draw_shortest_path(G, pos, start, end)
        This function draws the plot of the shortest path seperate from the initial plot
    
    edge_colors(G, path)
        This function colors the edges on the graph based on their role in the shortest path
    
    get_path_capacity(G, start, end)
        This function returns a list of the link capacities for each link in the shortest path
    
    get_path_pairs(path)
        This function gets the node pairs that make up the edges in the shortest path
    
    igrp_routing_calculation(G, pos, start, end)
        This function calculates the best path based on igrp given an input of graph and stard/end nodes
        it uses the all simple paths function to find all possible routes and then calcuates each routes
        metric given an igrp metric of available bandwidth (kbps) * delay (microseconds/10) 
        Metric = [K1 * Bandwidth + (K2 * Bandwidth)/(256-load) + K3*Delay] 
        where K1, K2, K3 are 1, 0, and 1 by default, load defaults to 1
    
    is_path_valid(g, pathquestion)
        This function checks to see if a user questions path is valid or not
    
    lowest_path_metric(igrp_path_metrics)
        This function takes the previous IGRP path metrics and finds the lowest one
    
    make_reference_graph_plot()
        This function defines the initial network plot based on the define_network function
    
    node_colors(G, path)
        This function colors the nodes on the graph based on their role in the shortest path
    
    print_all_simple_paths(G, startnode, endnode)
        This function returns all possible paths from the startnode to the end node as a list of lists

DATA
    G = <networkx.classes.graph.Graph object>
    bottleneckfound = ('b', 'c', '10 Gbps')
    endnode = 'c'
    igrp_default_path = [['a', 'b', 'c'], 5000006.68]
    igrp_path_metric = 5000006.68
    igrp_path_metrics = [[['a', 'b', 'c'], 5000006.68], [['a', 'b', 'd', '...
    latencyperkm = 3.34
    linkcapacity = [('a', 'b', '15 Gbps'), ('b', 'c', '10 Gbps')]
    pathquestion = ['a', 'b', 'c', 'd']
    pos = {'a': (1, 1), 'b': (1, 2), 'c': (2, 2), 'd': (2, 1), 'e': (4, 1)...
    startnode = 'a'

FILE
    /home/jwhite/SECUREMINDOWNCLOUD/DEVELOPMENT/NetworkSimPlayGround/network-plotting-examples.py


