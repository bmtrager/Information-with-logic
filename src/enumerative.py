"""Enumerative code size for constant-weight binary vectors.

A weight-``w`` vector of length ``n`` is one of ``C(n, w)`` possibilities, so it
can be indexed in ``ceil(log2 C(n, w))`` bits; ``enum_total_size`` adds an Elias
delta prefix that names the weight. These sizes price the enumerative source
codes reported in the figures.
"""

import math

from elias_delta import EliasDeltaEncode


def enum_size(n, w):
    """Bits needed to index a weight-``w`` vector of length ``n``."""
    return (math.comb(n, w) - 1).bit_length()


def enum_total_size(n, w):
    """Total enumerative code size: Elias delta weight prefix plus the index."""
    n = int(n)
    w = int(w)
    if w == 0:
        return 0
    return len(EliasDeltaEncode(w)) + enum_size(n, w)
