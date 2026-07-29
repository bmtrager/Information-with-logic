"""Elias gamma and delta codes for positive integers.

Only the encoders are used by the figure pipeline: the length of an integer's
delta code prices the size prefix of the enumerative and partition codes.
Codes are returned as bit strings.
"""

from math import floor, log


def Binary_Representation_Without_MSB(x):
    """Binary digits of ``x`` with the leading 1 removed."""
    return format(x, 'b')[1:]


def EliasGammaEncode(k):
    """Elias gamma code of ``k`` as a bit string."""
    if (k == 0):
        return '0'
    N = 1 + floor(log(k, 2))
    Unary = (N - 1) * '0' + '1'
    return Unary + Binary_Representation_Without_MSB(k)


def EliasDeltaEncode(k):
    """Elias delta code of ``k`` as a bit string."""
    Gamma = EliasGammaEncode(1 + floor(log(k, 2)))
    binary_without_MSB = Binary_Representation_Without_MSB(k)
    return Gamma + binary_without_MSB
