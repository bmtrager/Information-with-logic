import numpy as np
from random_encode_bernoulli import *
from elias_delta import *

def ind_to_bvector (size, ind) :
    v = np.zeros(size, dtype=bool)
    if (len(ind) > 0) :
        v[np.array(ind)]=True
    return v

def ind_to_bvector_comp (size, ind) :
    v = np.ones(size, dtype=bool)
    if (len(ind) > 0) :
        v[np.array(ind)]=False
    return v

# pind, mind are list of ints of true positions
# size is the space of possible zeros
def partition_encode(pind, mind, size, prob, seed) :
    pbv = ind_to_bvector(size, pind)
    mbv = ind_to_bvector_comp(size, mind)
    vec = np.array(pbv, dtype=np.uint8)
    ind = np.nonzero(pbv | mbv)[0]
    w = random_encode_select(vec, ind, prob, seed)
    return w

def partition_encode_size(pind, mind, size, prob, seed) :
    w = partition_encode(pind, mind, size, prob, seed)
    ed = EliasDeltaEncode(w.size)
    sz = len(ed) + w.size
#    print("delta encode size = " + str(len(ed)))
#    print("total size = " + str(sz))
    return sz

# this version restricts to solutions in rind
def partition_encode_restrict(pind, mind, rind, N, prob, seed) :
    rv = np.array(rind)
    pbv = ind_to_bvector(N, pind)[rv]
    mbv = ind_to_bvector_comp(N, mind)[rv]
    vec = np.array(pbv, dtype=np.uint8)
    ind = np.nonzero(pbv | mbv)[0]
# patch to test skipping random conde construction
#    w = ind
    w = random_encode_select(vec, ind, prob, seed)
    print("encode_delta = " + str(w.size-ind.size))
    return w

# this version restricts to solutions not in rind
def partition_encode_restrict_comp(pind, mind, rind, N, prob, seed) :
    rbvc = ind_to_bevctor_comp(N, rind)
    pbv = ind_to_bvector(N, pind)[rbvc]
    mbv = ind_to_bvector_comp(N, mind)[rbvc]
    vec = np.array(pbv, dtype=np.uint8)
    ind = np.nonzero(pbv | mbv)[0]
    w = random_encode_select(vec, ind, prob, seed)
    return w

def partition_encode_restrict_size(pind, mind, rind, N, prob, seed) :
    w = partition_encode_restrict(pind, mind, rind, N, prob, seed)
    ed = EliasDeltaEncode(w.size)
    sz = len(ed) + w.size
# patch for skipping elias code
#    sz = w.size
#    print("delta encode size = " + str(len(ed)))
#    print("total size = " + str(sz))
    return sz

def partition_decode(wvec, size, prob, seed) :
    return random_decode(wvec, size, prob, seed)

def partition_decode_restrict(wvec, rind, prob, seed) :
    return random_decode(wvec, len(rind), prob, seed)

def test_partition_decode(pind, mind, N, prob, seed) :
    w = partition_encode(pind, mind, N, prob, seed)
    ww = partition_decode(w, N, prob, seed)
    
    true_locs = ind_to_bvector(N,pind)
    false_locs = ind_to_bvector_comp(N, mind)
    return (np.all(ww[true_locs])) & (np.all(np.logical_not(ww[false_locs])))

def test_partition_decode_restrict (pind, mind, rind, N, prob, seed) :
    w = partition_encode_restrict(pind, mind, rind, N, prob, seed)
    ww = partition_decode_restrict(w, rind, prob, seed)

    rv = np.array(rind)
    true_locs = ind_to_bvector(N, pind)[rv]
    false_locs = ind_to_bvector_comp(N, mind)[rv]
    return (np.all(ww[true_locs])) & (np.all(np.logical_not(ww[false_locs])))
