import numpy as np
from gf2elim import *
import json
from readjson import *
from elias_delta import *

# v is a binary integer vector
# returns representation of v as combination of rows of random matrix
# needs common seed with decoder, np.random.seed(xxx)

# n is size of hash
# multiplies row vector v with random matrix 
# v is vector of sender's points
def hash_encode(v, n, s) :
    np.random.seed(s)

    v = np.array(v,dtype=np.uint8)
    M = np.random.randint(2, size=(v.size, n),dtype=np.uint8)
    return np.mod(np.dot(v, M), 2)

# h is hash from encoder
# w is vector of receivers points
def hash_decode(h, w, s) :
    np.random.seed(s)

    h = np.array(h, dtype=np.uint8)
    w = np.array(w, dtype=np.uint8)
    wb = np.array(w, dtype=bool)
    
    M = np.random.randint(2, size=(w.size, h.size),dtype=np.uint8)
    M = M[wb,:]

    Mv = np.vstack([M, h])
    n,m = Mv.shape

    Mv = gf2elim_rels(Mv)

    
#    print(Mv[:,0:m])
    
    rowsums = np.sum(Mv[:,0:m], axis=1)
#    print(rowsums)
    
    z_ind = np.where(rowsums==0)[0]
#    print(z_ind)
    
   # tests full rank before appending row and row in span
    if z_ind.size==1 and Mv[z_ind[0],n+m-1] == 1 :
        w_ind = np.nonzero(w)[0]
        x = Mv[z_ind[0],m:n+m-1]
        xb = ~np.array(x, dtype=bool)
        w_ind = w_ind[xb]
        w[w_ind] = 0
        return w

    return -1

def restricted_nullspace_empty(h, w, s) :
    np.random.seed(s)

    h = np.array(h, dtype=np.uint8)
    w = np.array(w, dtype=np.uint8)
    wb = np.array(w, dtype=bool)
    
    M = np.random.randint(2, size=(w.size, h.size),dtype=np.uint8)
    M = M[wb,:]
    n,m = M.shape
# by construction solution exists (v[wb]) with v from hash_encode
# test if solution is unique
# success if left null space of Mv = 0, i.e. rows of Mv are linearly independent
    M = gf2elim(M)
#   print([i for i in range(n) if np.all(M[i,:] == 0)])
# sucess if last row of reduced Mv is nonzero
    return not np.all(M[-1,:] == 0)

def hash_encode_test(v, w, n, s) :
    h = hash_encode(v, n, s)
    z = hash_decode(h, w, s)
    return np.array_equal(z, v)

def ind_to_bvector (size, ind) :
    v = np.zeros(size, dtype=np.uint8)
    if (len(ind)>0) :
        v[np.array(ind)]=1
    return v

def ind_to_bvector_comp (size, ind) :
    v = np.ones(size, dtype=np.uint8)
    if (len(ind)) > 0 :
        v[np.array(ind)]=0
    return v


def sender_zeros(data, case_num) :
    case = get_test_case(data,0,case_num)
    return case['Sender Zeroes']

def sender_bits(data, case_num) :
    N = pow(2, getnvars(data))
    case = get_test_case(data,0,case_num)
    sender_zeros = case['Sender Zeroes']
    szer = szeros_to_ints(sender_zeros)
    return ind_to_bvector(N,szer)

def receiver_zeros(data, case_num) :
    case = get_test_case(data,0,case_num)
    return case['Receiver Zeroes']

def query_zeros(data, case_num) :
    case = get_test_case(data,0,case_num)
    return case['Query Zeroes']

def receiver_bits(data, case_num) :
    N = pow(2, getnvars(data))
    case = get_test_case(data,0,case_num)
    receiver_zeros = case['Receiver Zeroes']
    rzer = szeros_to_ints(receiver_zeros)
    return ind_to_bvector(N,rzer)

def test_hash_case(data, case_num, n) :
    N = pow(2, getnvars(data))
    case = get_test_case(data,0,case_num)
    sender_zeros = case['Sender Zeroes']
    receiver_zeros = case['Receiver Zeroes']

#    print(str(len(sender_zeros)) + " sender zeros")
#    print(str(len(receiver_zeros)) + " receiver zeros")

    szer = szeros_to_ints(sender_zeros)
    rzer = szeros_to_ints(receiver_zeros)

    sbit = ind_to_bvector(N,szer)
    rbit = ind_to_bvector(N,rzer)

    result = hash_encode_test(sbit, rbit, len(rzer) + n, s)
    if result==False: print(case_num)
    return result

def test_hash_null_space(data, case_num, n, s) :
    N = pow(2, getnvars(data))
    case = get_test_case(data,0,case_num)
    sender_zeros = case['Sender Zeroes']
    receiver_zeros = case['Receiver Zeroes']

    szer = szeros_to_ints(sender_zeros)
    rzer = szeros_to_ints(receiver_zeros)

    sbit = ind_to_bvector(N,szer)
    rbit = ind_to_bvector(N,rzer)

    result = restricted_nullspace_empty(hash_encode(sbit,len(rzer) + n, s), rbit, s)
    if result==False: print(case_num)
    return result

# n = 10 seems good when pr = .5
def hash_encode_null_space_decode(szer, rzer, N, n, s) :
    sbit = ind_to_bvector(N,szer)
    rbit = ind_to_bvector(N,rzer)
    if (len(rzer) + n >= N) :
        return N 
    encode_cost = len(rzer) + n
    if restricted_nullspace_empty(hash_encode(sbit,len(rzer) + n, s), rbit, s) :
        return encode_cost
    else :
        return (N + encode_cost)
    
def test_hash_null_space_decode(data, case_num, N, n, s) :
    case = get_test_case(data,0,case_num)
    sender_zeros = case['Sender Zeroes']
    receiver_zeros = case['Query Zeroes']

    szer = szeros_to_ints(sender_zeros)
    rzer = szeros_to_ints(receiver_zeros)

    return hash_encode_null_space_decode(szer, rzer, N, n, s)

def test_successes(data,n) :
    return sum([test_hash_case(data,i, 25) for i in range(number_cases(data,0))])

def avg_receiver_size(data) :
    sizes = [len(receiver_zeros(data,i)) for i in range(number_cases(data,0))]
    return sum(sizes)/len(sizes)

def avg_sender_size(data) :
    sizes = [len(sender_zeros(data,i)) for i in range(number_cases(data,0))]
    return sum(sizes)/len(sizes)

def avg_query_size(data) :
    sizes = [len(query_zeros(data,i)) for i in range(number_cases(data,0))]
    return sum(sizes)/len(sizes)

#print("number of cases is " + str(number_cases(data,0)))

#print("average receiver size is " + str(avg_receiver_size(data)))

#print("number of successes is " + str(test_successes(data,11)))

s = 236245325

from glob import *

files = glob("../data/*0.5.json")

s = 1011144
slack = 10
N = 1024
# if false to skip
if False:
    for f in files :
         with open(f, "r") as read_file:    
             data = json.load(read_file)
             count = number_cases(data,0)
             print(f)
             print("slack ",slack) 
             print("number of failures is ", sum([not test_hash_null_space(data, i, slack,s) for i in range(count)]))
             print("average normalized cost is ", sum([test_hash_null_space_decode(data, i, N, slack, s) for i in range(count)])/count/N)
             print("average normalized query size is ", avg_query_size(data)/N)        
