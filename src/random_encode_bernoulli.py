"""Bernoulli random linear code over GF(2).

The partition encoder represents the sender's zero pattern as a linear
combination of rows drawn from a random Bernoulli(``p``) matrix, restricted to
the coordinates the receiver cares about. ``random_encode_select`` returns the
combining coefficients, whose length is the code word size priced by the
partition code.
"""

import math

import numpy as np

from gf2elim import gf2elim_rels


def strip_tail_zeros(v):
    """Drop trailing zeros from ``v`` (the code word carries no information)."""
    nz = np.nonzero(v)[0]
    if nz.size > 0:
        v = v[0:nz[-1] + 1]
    return v


def random_encode_select(v, ind, p, s):
    """Encode ``v`` restricted to columns ``ind`` against a seeded random matrix.

    Seeds the RNG with ``s`` so the decoder can regenerate the same matrix,
    draws Bernoulli(``p``) rows, and reduces ``[M; v]`` over GF(2) until the
    appended row lands in the span of ``M`` on the restricted columns. Extra
    rows are added until a solution exists. Returns the combining coefficients.
    """
    np.random.seed(s)

    M = np.zeros([0, v.size], dtype=np.uint8)
    pad = math.ceil(len(ind) * .05)
    for x in range(len(ind) + pad):
        M = np.vstack([M, np.random.binomial(1, p, size=v.size)])

    while True:
        Mv = np.vstack([M, v])
        Mv = Mv[:, ind]
        n, m = Mv.shape

        Mv = gf2elim_rels(Mv)

        if not np.any(Mv[n - 1, 0:m]) and Mv[n - 1, n + m - 1] == 1:
            return strip_tail_zeros(Mv[n - 1, m:n + m - 1])

        for x in range(pad):
            M = np.vstack([M, np.random.binomial(1, p, size=v.size)])
