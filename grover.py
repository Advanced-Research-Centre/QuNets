'''
Code: N qubit Grover search where the Oracle searches for the all-1s entry in an equal superposition
Purpose: scalable algorithm for testing QC simulator limits
Developer: Aritra Sarkar
'''

from qiskit import QuantumCircuit
from math import ceil, floor, sqrt, pi

'''
Decompose multi-controlled CNOT to Toffoli
https://algassert.com/circuits/2015/06/05/Constructing-Large-Controlled-Nots.html
'''
def nCX(c,t,b):
	nc = len(c)
	if nc == 1:
		qcirc.cx(c[0], t[0])
	elif nc == 2:
		qcirc.ccx(c[0],c[1],t[0])
	else:
		nch = ceil(nc/2)
		c1 = c[:nch]
		c2 = c[nch:]
		c2.append(b[0])
		# print([c1,b,nch+1],[c2,t,nch])
		nCX(c1,b,[c[nch]])
		nCX(c2,t,[c[nch-1]])
		nCX(c1,b,[c[nch]])
		nCX(c2,t,[c[nch-1]])
	return

'''
https://www.quantum-inspire.com/kbase/grover-algorithm/
'''
def grover():
    # Initialize
    for i in range(0,NUM_QB):
        qcirc.h(i)
    qcirc.barrier()

    # Grover iteration
    num_iter = floor(sqrt(2**NUM_QB)*pi/4)
    for j in range(0,num_iter):
        # Oracle
        qcirc.h(NUM_QB-1)
        nCX(list(range(0,NUM_QB-1)),[NUM_QB-1],[NUM_QB])
        qcirc.h(NUM_QB-1)
        qcirc.barrier()
        # Diffusion
        for i in range(0,NUM_QB):
            qcirc.h(i)
            qcirc.x(i)
        qcirc.h(NUM_QB-1)
        nCX(list(range(0,NUM_QB-1)),[NUM_QB-1],[NUM_QB])
        # nCX(list(range(1,NUM_QB)),[0],[NUM_QB])
        qcirc.h(NUM_QB-1)
        for i in range(0,NUM_QB):
            qcirc.x(i)
            qcirc.h(i)
        qcirc.barrier()
    # Measure (if you want the full state vector from simulator, comment out this part)
    for i in range(0,NUM_QB):
        qcirc.measure(i,i)

NUM_QB = int(input("Number of qubits: ") or 9)

print(NUM_QB,"qubit Grover search where the Oracle searches for the all-1s entry in an equal superposition")
qcirc = QuantumCircuit(NUM_QB+1,NUM_QB)
grover()

'''
OpenQASM and Circuit drawing
'''
print(qcirc.qasm())       # NOTE: Uncomment if required
# print(qcirc.draw())       # NOTE: Uncomment if required

'''
Execution result
'''

from qiskit import Aer, execute

backend = Aer.get_backend('qasm_simulator')  
job = execute(qcirc, backend, shots=1000, memory=True)
result = job.result()
print(result.get_counts())

'''
Visualization
'''

# from qiskit.visualization import plot_histogram

# import matplotlib.pyplot as plt
# plot_histogram(result.get_counts(), number_to_keep = 2**NUM_QB)
# plt.show()

'''
Execution results

works till 17 qubits, doesn't give execution result after that on my laptop
printing out the OpenQASM works
'''

# (qeait) D:\GoogleDrive\RESEARCH\A1 - Programs\QuNets>python grover.py
# Number of qubits: 2
# 2 qubit Grover search where the Oracle searches for the all-1s entry in an equal superposition
# {'11': 1000}

# (qeait) D:\GoogleDrive\RESEARCH\A1 - Programs\QuNets>python grover.py
# Number of qubits: 3
# 3 qubit Grover search where the Oracle searches for the all-1s entry in an equal superposition
# {'000': 6, '001': 9, '010': 6, '011': 10, '100': 4, '101': 5, '110': 9, '111': 951}

# (qeait) D:\GoogleDrive\RESEARCH\A1 - Programs\QuNets>python grover.py
# Number of qubits: 4
# 4 qubit Grover search where the Oracle searches for the all-1s entry in an equal superposition
# {'0000': 4, '0010': 2, '0011': 1, '0100': 1, '0101': 2, '0111': 2, '1000': 1, '1001': 4, '1010': 2, '1011': 2, '1100': 3, '1101': 3, '1110': 1, '1111': 972}

# (qeait) D:\GoogleDrive\RESEARCH\A1 - Programs\QuNets>python grover.py
# Number of qubits: 5
# 5 qubit Grover search where the Oracle searches for the all-1s entry in an equal superposition
# {'11111': 1000}

# (qeait) D:\GoogleDrive\RESEARCH\A1 - Programs\QuNets>python grover.py
# Number of qubits: 6
# 6 qubit Grover search where the Oracle searches for the all-1s entry in an equal superposition
# {'010001': 1, '010101': 1, '100000': 1, '111111': 994, '000111': 1, '001001': 1, '001101': 1}

# (qeait) D:\GoogleDrive\RESEARCH\A1 - Programs\QuNets>python grover.py
# Number of qubits: 7
# 7 qubit Grover search where the Oracle searches for the all-1s entry in an equal superposition
# {'0011110': 1, '1011001': 1, '1111111': 998}

# (qeait) D:\GoogleDrive\RESEARCH\A1 - Programs\QuNets>python grover.py
# Number of qubits: 8
# 8 qubit Grover search where the Oracle searches for the all-1s entry in an equal superposition
# {'11111111': 1000}

# (qeait) D:\GoogleDrive\RESEARCH\A1 - Programs\QuNets>python grover.py
# Number of qubits: 9
# 9 qubit Grover search where the Oracle searches for the all-1s entry in an equal superposition
# {'100110001': 1, '111111111': 999}

# (qeait) D:\GoogleDrive\RESEARCH\A1 - Programs\QuNets>python grover.py
# Number of qubits: 10
# 10 qubit Grover search where the Oracle searches for the all-1s entry in an equal superposition
# {'1111111111': 1000}

# (qeait) D:\GoogleDrive\RESEARCH\A1 - Programs\QuNets>python grover.py
# Number of qubits: 11
# 11 qubit Grover search where the Oracle searches for the all-1s entry in an equal superposition
# {'11111111111': 1000}

# (qeait) D:\GoogleDrive\RESEARCH\A1 - Programs\QuNets>python grover.py
# Number of qubits: 12
# 12 qubit Grover search where the Oracle searches for the all-1s entry in an equal superposition
# {'111111111111': 1000}

# (qeait) D:\GoogleDrive\RESEARCH\A1 - Programs\QuNets>python grover.py
# Number of qubits: 13
# 13 qubit Grover search where the Oracle searches for the all-1s entry in an equal superposition
# {'1111111111111': 1000}

# (qeait) D:\GoogleDrive\RESEARCH\A1 - Programs\QuNets>python grover.py
# Number of qubits: 14
# 14 qubit Grover search where the Oracle searches for the all-1s entry in an equal superposition
# {'11111111111111': 1000}

# (qeait) D:\GoogleDrive\RESEARCH\A1 - Programs\QuNets>python grover.py
# Number of qubits: 15
# 15 qubit Grover search where the Oracle searches for the all-1s entry in an equal superposition
# {'111111111111111': 1000}

# (qeait) D:\GoogleDrive\RESEARCH\A1 - Programs\QuNets>python grover.py
# Number of qubits: 16
# 16 qubit Grover search where the Oracle searches for the all-1s entry in an equal superposition
# {'1111111111111111': 1000}

# (qeait) D:\GoogleDrive\RESEARCH\A1 - Programs\QuNets>python grover.py
# Number of qubits: 17
# 17 qubit Grover search where the Oracle searches for the all-1s entry in an equal superposition
# {'11111111111111111': 1000}