import itertools
from pprint import pprint
from qiskit import QuantumCircuit, Aer, execute
backend = Aer.get_backend('qasm_simulator')  

maxgc = 5
gs = ['x','ccx']
qbnos = 4
qb = list(range(0,qbnos))

def toStr(n,base):
    '''
    Convert a decimal number to base-n
    '''
    convertString = "0123456789ABCDEF"
    if n < base:
        return convertString[n]
    else:
        return toStr(n//base,base) + convertString[n%base]

def X_choice(opcode):
    c = list(itertools.combinations(qb, 1))
    allc = []
    for i in c:
        allc.append(opcode+str(i[0]))
    return allc

def CCX_choice(opcode):
    c = list(itertools.combinations(qb, 3))
    allc = []
    for i in c:
        allc.append(opcode+str(i[0])+str(i[1])+str(i[2]))
        allc.append(opcode+str(i[1])+str(i[2])+str(i[0]))
        allc.append(opcode+str(i[2])+str(i[0])+str(i[1]))
    return allc

setX = X_choice('0')
setCCX = CCX_choice('1')

def progs(gc):
    p = []
    for i in range(0,len(gs)**gc):
        gseq = toStr(i,len(gs)).zfill(gc)
        cg = ['']          
        for j in range(0, len(gseq)):
            if gseq[j] == '0':
                g = list(itertools.product(cg, setX))
            if gseq[j] == '1':
                g = list(itertools.product(cg, setCCX))
            cg = []
            for k in g:
                cg.append(''.join(map(str, k)))
        # print(gseq,': ',cg)
        for j in cg:
            p.append(j)
    return p

def conv2QP(desc):
    qcirc = QuantumCircuit(qbnos,qbnos)
    i = 0
    while (i < len(desc)):
        if desc[i]=='0':
            # print('X',desc[i+1])
            qcirc.x(int(desc[i+1]))
            i+= 2
        elif desc[i]=='1':
            # print('CCX',desc[i+1],desc[i+2],desc[i+3])
            qcirc.ccx(int(desc[i+1]),int(desc[i+2]),int(desc[i+3]))
            i+= 4
    qcirc.barrier()
    for i in range(0,qbnos):
        qcirc.measure(i,i)
    return qcirc
     
def runQprog(desc):
    qcirc = conv2QP(desc)
    # print(desc)
    # print(qcirc.draw())
    job = execute(qcirc, backend, shots=1, memory=True)
    result = job.result()
    memory = result.get_memory()
    return memory[0][::-1] 

ng = {}
for gc in range(1,maxgc+1):
    p = progs(gc)
    for i in p:
        op = runQprog(i)
        if op in ng:
            ng[op].append(i)
        else:
            ng[op] = [i]
    print("nGC Level",gc)
    for key, value in sorted(ng.items()):
        value.sort(key=len)
        print(key, len(value),value[0],len(value[0]))


# pprint(ng)

'''
(qeait) D:\GoogleDrive\RESEARCH\A1 - Programs\QuNets>python d.py

00000 28385 1012
00001 2774 04
00010 2774 03
00011 176 0304
00100 2774 02
00101 176 0204
00110 176 0203
00111 12 020304
01000 2774 01
01001 176 0104
01010 176 0103
01011 12 010304
01100 176 0102
01101 12 010204
01110 12 010203
10000 2774 00
10001 176 0004
10010 176 0003
10011 12 000304
10100 176 0002
10101 12 000204
10110 12 000203
11000 176 0001
11001 12 000104
11010 12 000103
11100 12 000102

(qeait) D:\GoogleDrive\RESEARCH\A1 - Programs\QuNets>python d.py

GC Level 1
0000 12 1012
0001 1 03
0010 1 02
0100 1 01
1000 1 00

GC Level 2
0000 160 1012
0001 25 03
0010 25 02
0011 2 0203
0100 25 01
0101 2 0103
0110 2 0102
1000 25 00
1001 2 0003
1010 2 0002
1100 2 0001

GC Level 3
0000 2032 1012
0001 467 03
0010 467 02
0011 70 0203
0100 467 01
0101 70 0103
0110 70 0102
0111 12 010203
1000 467 00
1001 70 0003
1010 70 0002
1011 12 000203
1100 70 0001
1101 12 000103
1110 12 000102

GC Level 4
0000 26264 1012
0001 7847 03
0010 7847 02
0011 1682 0203
0100 7847 01
0101 1682 0103
0110 1682 0102
0111 492 010203
1000 7847 00
1001 1682 0003
1010 1682 0002
1011 492 000203
1100 1682 0001
1101 492 000103
1110 492 000102
1111 192 00010203

GC Level 5
0000 346568 1012
0001 125475 03
0010 125475 02
0011 34482 0203
0100 125475 01
0101 34482 0103
0110 34482 0102
0111 13812 010203
1000 125475 00
1001 34482 0003
1010 34482 0002
1011 13812 000203
1100 34482 0001
1101 13812 000103
1110 13812 000102
1111 7872 00010203
'''
