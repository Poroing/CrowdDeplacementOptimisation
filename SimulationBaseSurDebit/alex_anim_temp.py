import networkx as nx
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import random


# Graph initialization
G = nx.Graph()
G.add_nodes_from([1, 2, 3, 4])
G.add_edges_from([(1,2),(1,3),(1,4),(2,4)])

pos = [(1,1),(2,4),(1,3),(2,1),(3,3)]
colors = [100,300,500,700]

nx.draw_networkx(G, pos , node_size=colors)

# Animation funciton
def animate(i):
    plt.gcf().clear()
    nx.draw_networkx(G, pos , node_size=[random.choice(colors) for j in range(3)])
    plt.pause(0.5)

 
for k in range(6):
    animate(k)
    plt.show()
    
##
def plus_Liste( list,a):
    for k in range(len(list)):
        list[k]+=a
##

import networkx as nx
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import random

taille = [ random.randint(10,50)*30 for k in range(9)]

# Graph initialization

G = nx.Graph()
G.add_nodes_from([1, 2, 3, 4, 5, 6, 7, 8, 9])
G.add_edges_from([(1,2), (3,4), (2,5), (4,5), (6,7), (8,9), (4,7), (1,7), (3,5), (2,7), (5,8), (2,9), (5,7)])

nx.draw_circular

nx.draw_circular(G , node_size=colors)

# Animation funciton
def animate(i):
    plt.gcf().clear()
    nx.draw_circular(G , node_size=taille)
    plus_Liste(taille,-100)
    print( taille[0])
    plt.pause(0.5)

 
for k in range(10):
    animate(k)
    plt.show()
    
    
##


































