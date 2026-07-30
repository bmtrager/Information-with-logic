"""Read raw test sets and summarize per-case compression sizes.

Two roles:

* Regeneration -- :func:`process_compressed` runs every encoder over a raw test
  set and writes a ``*_compressed_count.json`` summary (mean and per-case
  sizes for the partition, enumerative and hash codes, plus the TNF baselines).
* Plotting -- :func:`get_compressed_data` loads a precomputed summary for the
  figure scripts.

A test set is a JSON object with ``Variables``, the ``p_sender`` / ``p_query``
/ ``p_receiver`` densities, and a list of ``Test Cases`` giving each party's
zero pattern (as binary strings) and TNF descriptions.
"""

import json

from partition_encode import partition_encode_restrict_size
from enumerative import enum_total_size
from tnf_baselines import compress_data
from random_hash_encode import hash_encode_null_space_decode

# Shared RNG seed so encoder and decoder build the same random matrices; fixed
# for byte-for-byte reproducible summaries.
seed = 1011144

# Hash slack: extra bits added to the receiver kernel size for the hash code.
HASH_SLACK = 10


def szeros_to_ints(lz):
    """Parse a list of binary strings into the integers they index."""
    return [int(v, base=2) for v in lz]


def getvars(data):
    return data['Variables']


def get_test_set_num(data):
    return data['Test Set #']


def number_cases(data):
    return len(data['Test Cases'])


def get_receiver_prob(data):
    return data['p_receiver']


def get_sender_prob(data):
    return data['p_sender']


def get_query_prob(data):
    return data['p_query']


def get_test_case(data, ncase):
    return data['Test Cases'][ncase]


def compute_restrict_prob(data):
    """Bernoulli parameter for the random code, restricted to the receiver kernel."""
    p_r = get_receiver_prob(data)
    p_s = get_sender_prob(data)
    p_q = get_query_prob(data)
    p_qc = p_r - p_q
    return p_s / (p_s + p_qc)


def process_case_size(data, ncase):
    """Encoded size of one test case under each code, as a dict of bit counts."""
    vars = getvars(data)
    N = pow(2, len(vars))
    case = get_test_case(data, ncase)
    sender_zeros = case['Sender Zeroes']
    receiver_zeros = case['Receiver Zeroes']
    if get_sender_prob(data) == get_query_prob(data):
        query_zeros = sender_zeros
    else:
        query_zeros = case['Query Zeroes']

    szer = szeros_to_ints(sender_zeros)
    qzer = szeros_to_ints(query_zeros)
    rzer = szeros_to_ints(receiver_zeros)

    prob = compute_restrict_prob(data)

    return dict(hash_sq=hash_encode_null_space_decode(szer, qzer, N, HASH_SLACK, seed),
                hash_sr=hash_encode_null_space_decode(szer, rzer, N, HASH_SLACK, seed),
                partition=partition_encode_restrict_size(szer, qzer, rzer, N, prob, seed),
                enum_sender=enum_total_size(len(rzer), len(szer)),
                enum_sender_only=enum_total_size(N, len(szer)),
                enum_query_compl=enum_total_size(len(rzer), len(rzer) - len(qzer)))


def process_case_size_rang(data, rang):
    return [process_case_size(data, i) for i in rang]


def mean(values):
    return sum(values) / len(values)


def mean_skip_zero(values):
    """Mean that ignores zero entries in the denominator (skips empty cases)."""
    return sum(values) / len([i for i in values if i != 0])


def process_full_set_size(data):
    """Aggregate per-case sizes across a test set into mean and normalized stats."""
    N = pow(2, len(getvars(data)))
    encoder_size_list = process_case_size_rang(data, range(number_cases(data)))
    hash_sq_sizes = [d['hash_sq'] for d in encoder_size_list]
    hash_sq_mean = mean(hash_sq_sizes)
    hash_sr_sizes = [d['hash_sr'] for d in encoder_size_list]
    hash_sr_mean = mean(hash_sr_sizes)
    partition_sizes = [d['partition'] for d in encoder_size_list]
    partition_mean = mean(partition_sizes)
    enum_sender_sizes = [d['enum_sender'] for d in encoder_size_list]
    enum_sender_mean = mean(enum_sender_sizes)
    enum_sender_only_sizes = [d['enum_sender_only'] for d in encoder_size_list]
    enum_sender_only_mean = mean(enum_sender_only_sizes)
    enum_query_compl_sizes = [d['enum_query_compl'] for d in encoder_size_list]
    enum_query_compl_mean = mean_skip_zero(enum_query_compl_sizes)

    return dict(test_set=get_test_set_num(data),
                num_vars=len(getvars(data)),
                p_receiver=get_receiver_prob(data),
                p_sender=get_sender_prob(data),
                p_query=get_query_prob(data),
                hash_sq_mean=hash_sq_mean,
                hash_sq_mean_normalized=hash_sq_mean / N,
                hash_sr_mean=hash_sr_mean,
                hash_sr_mean_normalized=hash_sr_mean / N,
                partition_mean=partition_mean,
                partition_mean_normalized=partition_mean / N,
                enum_sender_mean=enum_sender_mean,
                enum_sender_mean_normalized=enum_sender_mean / N,
                enum_sender_only_mean=enum_sender_only_mean,
                enum_sender_only_mean_normalized=enum_sender_only_mean / N,
                enum_query_compl_mean=enum_query_compl_mean,
                enum_query_compl_mean_normalized=enum_query_compl_mean / N,
                partition_sizes=partition_sizes,
                hash_sq_sizes=hash_sq_sizes,
                enum_sender_sizes=enum_sender_sizes,
                enum_query_compl_sizes=enum_query_compl_sizes)


def process_compressed(name):
    """Regenerate the ``*_compressed_count.json`` summary for test set ``name``."""
    with open(name + ".json", "r") as read_file:
        data = json.load(read_file)
    with open(name + "_compressed_count.json", "w") as outfile:
        json.dump(process_full_set_size(data) | compress_data(data), outfile)


def get_compressed_data(fn, ps, pq, pr):
    """Load the precomputed summary for the (``ps``, ``pq``, ``pr``) test set."""
    fn += str(ps) + "-" + str(pq) + "-" + str(pr) + "_compressed_count.json"
    with open(fn, "r") as read_file:
        data = json.load(read_file)
    return data
