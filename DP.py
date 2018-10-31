import numpy as np
import math

'''############################################################################
    Need to parse the data extracting node count, start node, and goal from the
    first three lines. The rest of the lines (4->inf) is edge info
############################################################################'''
_input_data_file = open("input.txt")
n       =   int(_input_data_file.readline())
start   =   int(_input_data_file.readline())
goal    =   int(_input_data_file.readline())

weighted_edge_list = np.genfromtxt(r'input.txt', delimiter=' ', skip_header=3)

_input_data_file.close()

'''###############################
    need to setup some variables
##################################'''
rows = n
columns = n-1
inf = math.inf
node_list = set(weighted_edge_list[:,0])
shortest_path = {}

dp_table = np.zeros(dtype='float', shape=[rows,columns])

'''########################################################################
    Bulk of Dynamic programming run here. After parsing the input file,
    the outgoing edges are placed into a dictionary with a key for each node.
    In this way, as the cost to go from a node is calculated, the dictionary
    can be called directly for relevant edges. The starting column is the
    rightmost column. All rows which correspond to each node, is evaluated
    for each column before moving to the next column. The goal column is
    initiated with zero for the goal, and inf. for all others.
########################################################################'''
outgoing_edges = {}
min_cost = {}

#want a dictionary of the outgoing edges keyed by the node number
for x in range(1,n+1):
    ix = np.isin(weighted_edge_list[:,0],x)
    outgoing_edges[x] = np.where(ix)

#the minimum cost to go from each node is the edge cost to go from xi to xj,
#plus the cost to go from xj to the goal.
def get_lowest_cost(k, xi):
    V = 0.0
    V_min = inf

    #check all outgoing edges.
    for x in range(len(outgoing_edges[xi][0])):
        V = weighted_edge_list[outgoing_edges[xi][0][x],2] + dp_table[int(weighted_edge_list[outgoing_edges[xi][0][x],1]-1),columns-k]
        #want to update minimum cost to go if the calculated cost is less than the current minimum cost
        if V <V_min: #update minimum value and shortest path pointer
            V_min = V
            shortest_path[xi] = int(weighted_edge_list[outgoing_edges[xi][0][x],1])
    return V_min

for k in range(columns): #evaluate all rows for each column
    for x in range(1,n+1):
        if x == goal:
            dp_table[x-1,columns-1-k]=0.0
            continue
        elif k == 0 and x != goal:
            dp_table[x-1,columns-1-k] = inf
            continue
        else:
            pass
            dp_table[x-1,columns-1-k] = get_lowest_cost(k,x)

'''###############################################
    Get the shortes path by gathering the
    pointers from the stating node until the goal.
    write shortest path to a text file on line 1.
    write the value function on line 2
###############################################'''
pointer = start

#print('start ', start)
#print('goal ',goal)

f = open("output.txt", "w")
f.write(str(start))
f.write(' ')

while pointer != goal:
    #print(shortest_path[pointer])
    f.write(str(shortest_path[pointer]))
    f.write(' ')
    pointer = shortest_path[pointer]

f.write('\n')

np.savetxt(f,dp_table[:,0],fmt='%0.6f',delimiter=' ',newline=' ')
f.close
