'''
import pyasn
asndb = pyasn.pyasn('/home/jwhite/asn_analysis/asn.dat')
print(asndb.lookup('8.8.8.8'))
print(asndb.get_as_prefixes(15169))
'''

import itertools 
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import pylab

G = nx.Graph()

with open('asn.dat') as f: # open the file for reading
    for line in itertools.islice(f, 6, None): #start on the 7th line of the dat file
        linesplit = line.split("\t")
        #print(linesplit[0].rstrip('\n'))
        G.add_edge(linesplit[0].rstrip('\n'), linesplit[1].rstrip('\n'))

print("There were :", nx.number_of_nodes(G), "nodes added to the graph")
print("There were :", nx.number_of_edges(G), "edges added to the graph")


def save_graph(graph,file_name):
    #initialze Figure
    plt.figure(num=None, figsize=(20, 20), dpi=80)
    plt.axis('off')
    fig = plt.figure(1)
    pos = nx.spring_layout(graph)
    nx.draw_networkx_nodes(graph,pos)
    nx.draw_networkx_edges(graph,pos)
    nx.draw_networkx_labels(graph,pos)

    cut = 1.00
    xmax = cut * max(xx for xx, yy in pos.values())
    ymax = cut * max(yy for xx, yy in pos.values())
    plt.xlim(0, xmax)
    plt.ylim(0, ymax)

    plt.savefig(file_name,bbox_inches="tight")
    pylab.close()
    del fig

save_graph(G,"output.pdf")   
    
#nx.draw(G)
#plt.show()

