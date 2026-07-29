import numpy as np
#import numba

#@numba.jit(nopython=True, parallel=True) #parallel speeds up computation only over very large matrices
# M is a mxn matrix binary matrix 
# all elements in M should be uint8 
def gf2elim(M):

    m,n = M.shape

    i=0
    j=0

    while i < m and j < n:
        # find value and index of largest element in remainder of column j
        k = np.argmax(M[i:, j]) +i

        # swap rows
        M[[k, i]] = M[[i, k]]

        # use this for numba instead
        # temp = np.copy(M[k])
        # M[k] = M[i]
        # M[i] = temp

        if M[i,j] != 0 :

            aijn = M[i, j:]

            col = np.copy(M[:, j]) #make a copy otherwise M will be directly affected

            col[i] = 0 #avoid xoring pivot row with itself

            flip = np.outer(col, aijn)

            M[:, j:] = M[:, j:] ^ flip

            i += 1
            j +=1
            
        else:
            j +=1

    return M

def gf2elim_rels(M):

    m,n = M.shape
    # extend matrix with identity to find relations
    M = np.hstack([M, np.eye(m, dtype=np.uint8)])

    i=0
    j=0

    while i < m and j < n:
        # find value and index of largest element in remainder of column j
        k = np.argmax(M[i:, j]) +i

        # swap rows
        M[[k, i]] = M[[i, k]]

        # use this for numba instead
        # temp = np.copy(M[k])
        # M[k] = M[i]
        # M[i] = temp
     

        if M[i,j] != 0 :

            aijn = M[i, j:]

            col = np.copy(M[:, j]) #make a copy otherwise M will be directly affected

            col[i] = 0 #avoid xoring pivot row with itself

            flip = np.outer(col, aijn)

            M[:, j:] = M[:, j:] ^ flip

            j +=1
            i += 1
        else:
            j +=1

    return M
