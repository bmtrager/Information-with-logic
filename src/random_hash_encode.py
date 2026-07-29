"""Random linear hash for the "no need to know" scheme.

The sender hashes its zero pattern through a seeded random GF(2) matrix. The
receiver can recover the pattern iff, restricted to its own known coordinates,
the hash pins down a unique solution -- i.e. the restricted left null space is
empty. ``hash_encode_null_space_decode`` prices this: the hash cost on success,
or a full ``N``-bit fallback on failure.
"""

import numpy as np

from gf2elim import gf2elim


def hash_encode(v, n, s):
    """Hash the binary vector ``v`` to ``n`` bits via a seeded random matrix."""
    np.random.seed(s)

    v = np.array(v, dtype=np.uint8)
    M = np.random.randint(2, size=(v.size, n), dtype=np.uint8)
    return np.mod(np.dot(v, M), 2)


def restricted_nullspace_empty(h, w, s):
    """True iff the hash ``h`` has a unique preimage on the support of ``w``.

    Regenerates the same random matrix from seed ``s``, keeps the rows selected
    by ``w``, and reduces over GF(2). A solution exists by construction; it is
    unique iff those rows are linearly independent, i.e. the reduced last row is
    nonzero.
    """
    np.random.seed(s)

    h = np.array(h, dtype=np.uint8)
    w = np.array(w, dtype=np.uint8)
    wb = np.array(w, dtype=bool)

    M = np.random.randint(2, size=(w.size, h.size), dtype=np.uint8)
    M = M[wb, :]
    M = gf2elim(M)
    return not np.all(M[-1, :] == 0)


def ind_to_bvector(size, ind):
    """uint8 indicator vector of length ``size`` set to 1 at positions ``ind``."""
    v = np.zeros(size, dtype=np.uint8)
    if (len(ind) > 0):
        v[np.array(ind)] = 1
    return v


def hash_encode_null_space_decode(szer, rzer, N, n, s):
    """Cost of hashing sender zeros ``szer`` for a receiver with kernel ``rzer``.

    Uses a hash of ``len(rzer) + n`` bits. Returns that cost when the receiver
    can decode uniquely, and ``N + cost`` (a full-description fallback) when it
    cannot; ``N`` when the hash would not be smaller than the space itself.
    """
    sbit = ind_to_bvector(N, szer)
    rbit = ind_to_bvector(N, rzer)
    if (len(rzer) + n >= N):
        return N
    encode_cost = len(rzer) + n
    if restricted_nullspace_empty(hash_encode(sbit, len(rzer) + n, s), rbit, s):
        return encode_cost
    else:
        return (N + encode_cost)
