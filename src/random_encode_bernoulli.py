import numpy as np
import math
from gf2elim import *

# v is a binary integer vector
# p is prob of 1
# returns representation of v as combination of rows of random matrix
# needs common seed with decoder, np.random.seed(xxx)
    
def strip_tail_zeros (v) :
    nz = np.nonzero(v)[0]
    if nz.size > 0: 
        v = v[0:nz[-1]+1]
#        print("strip size = " + str(v.size))
    return v

def random_encode(v, p, s):

    np.random.seed(s)
#    pad = int(v.size * .05)
    pad = math.ceil(v.size * .05)
    M = np.zeros([0,v.size], dtype=np.uint8)
    for x in range(v.size + pad) :
        M = np.vstack([M, np.random.binomial(1, p, size=v.size)])

    while True :

        Mv = np.vstack([M, v])
        n,m = Mv.shape

#        Mv = gf2elim( np.hstack([Mv, np.eye(n, dtype=np.uint8)]))
        Mv = gf2elim_rels(Mv)

        if not np.any(Mv[n-1,0:m]) and Mv[n-1, n+m-1] == 1:
            print(Mv)
            return strip_tail_zeros(Mv[n-1, m:n+m-1])

        print("adding " + str(pad) + " rows")
        for x in range(pad):
            M = np.vstack([M, np.random.binomial(1, p, size=v.size)])

    return np.zeros(0)

# ind is a list of columns to restrict to

def random_encode_select(v, ind, p, s):

    np.random.seed(s)

    M = np.zeros([0,v.size], dtype=np.uint8)
#    pad = int(len(ind)*.05)
    pad = math.ceil(len(ind)*.05)
#    print("pad = " + str(pad))
    for x in range(len(ind)+pad) :
        M = np.vstack([M, np.random.binomial(1, p, size=v.size)])

#    print("ind size = " + str(len(ind)))
    while True :

#        print ("M.shape = " + str(M.shape))
        Mv = np.vstack([M, v])
        Mv = Mv[:,ind]
        n,m = Mv.shape

#        Mv = gf2elim( np.hstack([Mv, np.eye(n, dtype=np.uint8)]))
        Mv = gf2elim_rels(Mv)

        if not np.any(Mv[n-1,0:m]) and Mv[n-1, n+m-1] == 1:
#            print("final size = " + str(n-1))
            return strip_tail_zeros(Mv[n-1, m:n+m-1])

        print("adding " + str(pad) + " rows")
        for x in range(pad) :
            M = np.vstack([M, np.random.binomial(1, p, size=v.size)])

    return np.zeros(0)

# w is a binary vector of matrix coefficients
# n is size of vector to be generated
# needs common seed with encoder, np.random.seed(xxx)
     
def random_decode(w, n, p, s):

    np.random.seed(s)
    M = np.zeros([0,n], dtype=np.uint8)

    for x in range(w.size) :
        M = np.vstack([M, np.random.binomial(1,p, size = n)])

    return np.mod(np.dot(w,M),2)

#p = .7
#v = np.array([1,0,1,1,0,1,1,1])
#s = 2334235
#w = random_encode(v, p, s)
#print(v)
#print(w)
#print(random_decode(w, v.size, p, s))

#ind = [2,3,4,7]
#ww = random_encode_select(v, ind, p, s)
#vv = random_decode(ww, v.size, p, s)
#print (ww)
#print (vv)
#print (v[ind])
#print (vv[ind])


      
