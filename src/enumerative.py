import math
import numpy as np
from elias_delta import *

#sorts rows of matrix in ascending lex order

def row_sort_lr(m):
    return m[np.lexsort(m.T[::-1])]

def row_sort_rl(m):
    return m[np.lexsort(m.T)]

# returns array of indices of target row in source
def find_rows(source, target):
    return np.where((source == target).all(axis=1))[0]

#enumeration of binary vectors of length n and constant weight w

def enum_index_coef (w, x, k):
    return math.comb(x.size - k, w - x[:(k-1)].sum())

def enum_index(x):
    w = x.sum()
    ind = 0
    for i in range(x.size):
        ind += x[i]*enum_index_coef(w, x, i+1)
    return ind

def enum_value(n, w, ind):
    y = np.zeros(n, dtype=int)
    for i in range(n):
        c = enum_index_coef(w, y, i+1)
        if ind >= c :
            y[i] = 1
            ind -= c
    return y

def enum_size(n, w) :
    return (math.comb(n,w)-1).bit_length()

def enum_total_size(n, w) :
    n = int(n)
    w = int(w)
    if w == 0:
        print("enum zero length")
        return 0
    return len(EliasDeltaEncode(w)) + enum_size(n,w)

if False :
    N=2**10
    p_r=1.0
    p_s=.15
    
    print("p_r = " + str(p_r))
    print("p_s = " + str(p_s))
    print("enumerate sender = " + str(enum_total_size(p_r*N, p_s*N)))
    
    p_r=.5
    p_s=.075
    print("p_r = " + str(p_r))
    print("p_s = " + str(p_s))
    print("enumerate sender = " + str(enum_total_size(p_r*N, p_s*N)))
    
    p_r=1.0
    print("p_r = " + str(p_r))
    for p_q in [.25, .35, .45, .55, .65, .75, .85, .95]:
        print("p_q = " + str(p_q))
        print("enumerate query_c = " + str(enum_total_size(p_r*N, (p_r-p_q)*N)))    
        
        p_r=0.5
        print("p_r = " + str(p_r))
        for p_q in [.25, .35, .45, .55, .65, .75, .85, .95]:
            p_q = p_q * p_r
            print("p_q = " + str(p_q))
            print("enumerate query_c = " + str(enum_total_size(p_r*N, (p_r-p_q)*N)))
    


#x = np.array([1,0,1,1,0,1,1])
#ind= enum_index(x)
#print(x)
#print(ind)
#print(enum_value(x.size,x.sum(),ind))


    
    
