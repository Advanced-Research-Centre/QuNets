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

def calc_rho(L, tau):
    '''
    Calculate Partition Function and Density Matrix from Graph Laplacian
    https://journals.aps.org/prx/pdf/10.1103/PhysRevX.6.041062
    '''
    rho = expm(-tau*L) / np.trace(expm(-tau*L))
    return rho

def calc_U(dm1, dm2):
    '''
    Find a unitary transform U between two matrices:
        U . G1 . Transpose[U] == G2
    The eigenvectors of the matrices G1, G2 are v1, v2
        v1 . G1 . Transpose[v1] == v2 . G2 . Transpose[v2]
    which means: 
        U = Transpose[v2] . v1
    '''
    _,evec_1 = np.linalg.eig(dm1)
    _,evec_2 = np.linalg.eig(dm2)
    U = np.dot(np.transpose(evec_2),evec_1)
    # U = np.inner(np.transpose(evec_c),evec_i)
    print("\nUnitary transform")
    print(U)
    # print("Test correctness:")
    # print(np.dot(U,np.transpose(U)))
    # rec_rho_c = np.dot(np.dot(U,rho_i),np.transpose(U))
    # rec_rho_c = np.dot(U,np.dot(rho_i,np.transpose(U)))
    # print(rec_rho_c)

G_i = build_ig()
G_c = build_cg()

L_i = calc_L(G_i)
L_c = calc_L(G_c)

rho_i = calc_rho(L_i, 1)
rho_c = calc_rho(L_c, 1)

# Super-easy test cases for sanity checks
rho_0 = np.array([[1,0],[0,0]])
rho_plus = 0.5*np.array([[1,1],[1,1]])
# print(np.trace(rho_0*rho_0))
# print(np.trace(np.dot(rho_plus,rho_plus)))
# rho_i = rho_0
# rho_c = rho_plus

print("\n ==== Interaction Graph: triangle")
print("\ngraph Lagrangian:\n",L_i)
print("\ngraph density matrix:\n",rho_i)
print("\npurity:",np.trace(np.dot(rho_i,rho_i)))

print("\n ==== Connectivity Graph: arc")
print("\ngraph Lagrangian:\n",L_c)
print("\ngraph density matrix:\n",rho_c)
print("\npurity:",np.trace(np.dot(rho_c,rho_c)))

# nx.draw(cg)
# plt.show()

# https://handwiki.org/wiki/Purification_of_quantum_state
# https://quantumcomputing.stackexchange.com/questions/14456/how-can-i-find-a-quantum-channel-connecting-two-arbitrary-quantum-states