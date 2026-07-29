"""Partition code for a sender/receiver zero pattern.

The sender's ``true`` positions and the receiver's known ``false`` positions
partition the coordinate space; the free coordinates are encoded with a random
linear code (:func:`random_encode_select`). ``partition_encode_restrict``
restricts the problem to the receiver's kernel ``rind`` and
``partition_encode_restrict_size`` prices the resulting code word plus its
Elias delta length prefix.
"""

import numpy as np

from random_encode_bernoulli import random_encode_select
from elias_delta import EliasDeltaEncode


def ind_to_bvector(size, ind):
    """Boolean vector of length ``size`` that is True at positions ``ind``."""
    v = np.zeros(size, dtype=bool)
    if (len(ind) > 0):
        v[np.array(ind)] = True
    return v


def ind_to_bvector_comp(size, ind):
    """Boolean vector of length ``size`` that is False at positions ``ind``."""
    v = np.ones(size, dtype=bool)
    if (len(ind) > 0):
        v[np.array(ind)] = False
    return v


def partition_encode_restrict(pind, mind, rind, N, prob, seed):
    """Encode the zero pattern restricted to the receiver kernel ``rind``.

    ``pind`` are the sender's true positions, ``mind`` the known false
    positions, ``rind`` the receiver kernel to restrict to, and ``N`` the full
    space size. Returns the random-code combining coefficients.
    """
    rv = np.array(rind)
    pbv = ind_to_bvector(N, pind)[rv]
    mbv = ind_to_bvector_comp(N, mind)[rv]
    vec = np.array(pbv, dtype=np.uint8)
    ind = np.nonzero(pbv | mbv)[0]
    w = random_encode_select(vec, ind, prob, seed)
    return w


def partition_encode_restrict_size(pind, mind, rind, N, prob, seed):
    """Size in bits of the restricted partition code plus its length prefix."""
    w = partition_encode_restrict(pind, mind, rind, N, prob, seed)
    ed = EliasDeltaEncode(w.size)
    sz = len(ed) + w.size
    return sz
