import networkx as nx
import matplotlib.pyplot as plt
from scipy.linalg import expm
import numpy as np

def build_ig():
    '''
    Interaction graph (of quantum algorithm)
    '''
    g = nx.Graph()
    g.add_node(0)
    g.add_node(1)
    g.add_node(2)
    g.add_edge(0,1)
    g.add_edge(0,2)
    g.add_edge(1,2)
    return g

def build_cg():
    '''
    Connectivity graph (of quantum processor)
    '''
    g = nx.Graph()
    g.add_node(0)
    g.add_node(1)
    g.add_node(2)
    g.add_edge(0,1)
    g.add_edge(0,2)
    return g

def calc_L(g):
    '''
    Graph Laplacian
    https://en.wikipedia.org/wiki/Laplacian_matrix
    '''
    A = nx.adjacency_matrix(g).todense()
    D = np.diag([g.degree(n) for n in g.nodes()])
    return D-A

ig = build_ig()
cg = build_cg()

Lig = calc_L(ig)
print(Lig)


ig_me = expm(-1*Lig)
print(ig_me)



# nx.draw(cg)
# plt.show()
