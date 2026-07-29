import json
import math
from partition_encode import *
from enumerative import *
from compress_data_concat_new_nocnf import *
#from compress_data_concat_new import *
#from compress_data import *
from random_hash_encode import *

#with open("test_set_0.15-0.55-1.0.json", "r") as read_file:
#    data = json.load(read_file)

def szeros_to_ints (lz) :
    return [int(v,base=2) for v in lz]

def getvars(data) :
    return data['Variables']

def getnvars(data) :
    return len(getvars(data))

def number_sets(data) :
    return len(data['Test Sets'])

def get_test_set(data, nset) :
#    return data['Test Sets'][nset]
    return data

def get_test_set_num(data, nset) :
    return get_test_set(data,nset)['Test Set #']

def number_cases(data, nset) :
    return len(get_test_set(data, nset)['Test Cases'])

def get_receiver_prob(data, nset) :
    return get_test_set(data,nset)['p_receiver']

def get_sender_prob(data, nset) :
    return get_test_set(data,nset)['p_sender']

def get_query_prob(data, nset) :
    return get_test_set(data,nset)['p_query']

def get_test_case(data, nset, ncase) :
    return get_test_set(data,nset)['Test Cases'][ncase]
    
def compute_prob(data, nset) :
    p_r = get_receiver_prob(data,nset)
    p_s = get_sender_prob(data, nset)
    p_q = get_query_prob(data, nset)
    p_qc = 1 - p_q
    return p_s/(p_s + p_qc)

def compute_restrict_prob(data, nset) :
    p_r = get_receiver_prob(data,nset)
    p_s = get_sender_prob(data, nset)
    p_q = get_query_prob(data, nset)
    p_qc = p_r - p_q
    return p_s/(p_s + p_qc)

seed = 1011144

def process_case(data,nset,ncase) :
    vars = getvars(data)
    N = pow(2, len(vars))
    
    case = get_test_case(data,nset,ncase)
    sender_zeros = case['Sender Zeroes']
    receiver_zeros = case['Receiver Zeroes']
    query_zeros = case['Query Zeroes'] 

    szer = szeros_to_ints(sender_zeros)
    qzer = szeros_to_ints(query_zeros)
    rzer = szeros_to_ints(receiver_zeros)

    prob = compute_restrict_prob(data,nset)
    
    w = partition_encode_restrict(szer, qzer, rzer, N, prob, seed)
    return w

def process_case_size(data,nset,ncase) :
    vars = getvars(data)
    N = pow(2, len(vars))
#    print ("set = " + str(nset))
    print ("case = " + str(ncase))
    case = get_test_case(data,nset,ncase)
    sender_zeros = case['Sender Zeroes']
    receiver_zeros = case['Receiver Zeroes']
    if get_sender_prob(data,nset) == get_query_prob(data,nset) :
        print("p_q = p_s")
        query_zeros = sender_zeros
    else :
        query_zeros = case['Query Zeroes']

    szer = szeros_to_ints(sender_zeros)
    qzer = szeros_to_ints(query_zeros)
    rzer = szeros_to_ints(receiver_zeros)

    prob = compute_restrict_prob(data,nset)
#    print("prob = " + str(prob))
    
    # 10 semms good delta for hash encoder
    return dict(hash_sq = hash_encode_null_space_decode(szer, qzer, N, 10, seed),
                hash_sr = hash_encode_null_space_decode(szer, rzer, N, 10, seed),                
                partition = partition_encode_restrict_size(szer, qzer, rzer, N, prob, seed),
                enum_sender = enum_total_size(len(rzer), len(szer)),
                enum_sender_only = enum_total_size(2**10, len(szer)),                
                enum_query_compl = enum_total_size(len(rzer), len(rzer)-len(qzer)))

def test_case(data,nset,ncase) :
    vars = getvars(data)
    N = pow(2, len(vars))
    
    case = get_test_case(data,nset,ncase)
    sender_zeros = case['Sender Zeroes']
    receiver_zeros = case['Receiver Zeroes']
    query_zeros = case['Query Zeroes']

    szer = szeros_to_ints(sender_zeros)
    qzer = szeros_to_ints(query_zeros)
    prob = compute_prob(data,nset)

    return test_partition_decode(szer, qzer, N, prob, seed)

def test_case_restrict(data,nset,ncase) :
    vars = getvars(data)
    N = pow(2, len(vars))
    
    case = get_test_case(data,nset,ncase)
    sender_zeros = case['Sender Zeroes']
    receiver_zeros = case['Receiver Zeroes']
    query_zeros = case['Query Zeroes']

    szer = szeros_to_ints(sender_zeros)
    qzer = szeros_to_ints(query_zeros)
    rzer = szeros_to_ints(receiver_zeros)
    
    prob = compute_restrict_prob(data,nset)
    return test_partition_decode_restrict(szer, qzer, rzer, N, prob, seed)

def process_case_size_rang(data,nset,rang) :
    return [process_case_size(data,nset,i) for i in rang]

def mean(list) :
    return sum(list)/len(list)

def mean_skip_zero(list) :
    return sum(list)/len([i for i in list if i != 0])

def std(list) :
    avg = mean(list)
    return math.sqrt((sum([(x-avg)**2 for x in list]))/(len(list)-1))

def process_full_set_size(data,nset) :
#    N = pow(2, len(getvars(data)))*get_receiver_prob(data,nset)
    N = pow(2, len(getvars(data)))
    encoder_size_list = process_case_size_rang(data,nset,range(number_cases(data,nset)))
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
    print("partition mean = ", partition_mean)
    print("partition std = ", std(partition_sizes))
    print("partition min = ", min(partition_sizes))
    print("partition max = ", max(partition_sizes))    

    return dict(test_set   = get_test_set_num(data,nset),
                num_vars   = len(getvars(data)),
                p_receiver = get_receiver_prob(data,nset),
                p_sender   = get_sender_prob(data, nset),
                p_query    = get_query_prob(data,nset),
                hash_sq_mean = hash_sq_mean,
                hash_sq_mean_normalized = hash_sq_mean/N,
                hash_sr_mean = hash_sr_mean,
                hash_sr_mean_normalized = hash_sr_mean/N,                
                partition_mean = partition_mean,
                partition_mean_normalized = partition_mean/N,
                enum_sender_mean = enum_sender_mean,
                enum_sender_mean_normalized = enum_sender_mean/N,
                enum_sender_only_mean = enum_sender_only_mean,
                enum_sender_only_mean_normalized = enum_sender_only_mean/N,
                enum_query_compl_mean = enum_query_compl_mean,
                enum_query_compl_mean_normalized = enum_query_compl_mean/N,
                partition_sizes=partition_sizes,
                hash_sq_sizes = hash_sq_sizes,
                enum_sender_sizes=enum_sender_sizes,
                enum_query_compl_sizes = enum_query_compl_sizes)

#print(test_case(data,0,0))
#print(test_case_restrict(data,0,0))
#print(process_full_set_size(data, 0))

def write_full_set_size(data,nset) :
    name = "test_set_" + str(get_test_set_num(data,nset)) + "_count.json"
    print(name)
    with open(name, "w") as outfile:
         json.dump(process_full_set_size(data,nset), outfile)

#write_full_set_size(data,0)

def process(name) :
    print(name)
    with open(name + ".json", "r") as read_file:
        data = json.load(read_file)
    with open(name + "_count.json", "w") as outfile:
        json.dump(process_full_set_size(data,0), outfile)
    
def process_compressed(name) :
    print(name)
    with open(name + ".json", "r") as read_file:
        data = json.load(read_file)
    with open(name + "_compressed_count.json", "w") as outfile:
        json.dump(process_full_set_size(data,0) | compress_data(data), outfile)

def get_compressed_data(fn, ps, pq, pr) :
    # fn = "../data/test_set_"
    fn += str(ps) + "-" + str(pq) + "-" + str(pr) + "_compressed_count.json"
    with open(fn, "r") as read_file:
        data = json.load(read_file)
    return data

def compare_sizes(oname, name) :
    with open(oname + ".json", "r") as read_file:
        odata = json.load(read_file)
        osizes = odata["sizes"]
    with open(name + ".json", "r") as read_file:
        data = json.load(read_file)
        sizes = data["partition_sizes"]
    if osizes == sizes:
        print("equal")
    else:
        print("not_equal")
        inds = [i for i in range(len(sizes)) if sizes[i] != osizes[i]]
        print ([[i,osizes[i],sizes[i]] for i in inds])

def get_data_from_file(name) :
    with open(name + ".json", "r") as read_file:
        return json.load(read_file)
