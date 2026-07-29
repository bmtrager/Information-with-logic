"""Gaussian elimination over GF(2) for uint8 binary matrices."""

import numpy as np


def gf2elim(M):
    """Row-reduce ``M`` (mod 2) in place and return it."""
    m, n = M.shape

    i = 0
    j = 0

    while i < m and j < n:
        # find the pivot in the remainder of column j
        k = np.argmax(M[i:, j]) + i

        # swap rows
        M[[k, i]] = M[[i, k]]

        if M[i, j] != 0:
            aijn = M[i, j:]
            col = np.copy(M[:, j])   # copy so M is not modified mid-update
            col[i] = 0               # do not xor the pivot row with itself
            flip = np.outer(col, aijn)
            M[:, j:] = M[:, j:] ^ flip
            i += 1
            j += 1
        else:
            j += 1

    return M


def gf2elim_rels(M):
    """Row-reduce ``M`` (mod 2) while recording the row combinations used.

    Appends an identity block so each reduced row records which original rows
    produced it; this is what lets the random linear code recover a code word.
    """
    m, n = M.shape
    # extend with an identity block to track row relations
    M = np.hstack([M, np.eye(m, dtype=np.uint8)])

    i = 0
    j = 0

    while i < m and j < n:
        k = np.argmax(M[i:, j]) + i

        M[[k, i]] = M[[i, k]]

        if M[i, j] != 0:
            aijn = M[i, j:]
            col = np.copy(M[:, j])
            col[i] = 0
            flip = np.outer(col, aijn)
            M[:, j:] = M[:, j:] ^ flip
            j += 1
            i += 1
        else:
            j += 1

    return M
