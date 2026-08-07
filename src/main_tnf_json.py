import sys
import random
from cnf import CNF
from clause import Clause
from truthSet import TruthSet
from query import Query
from tnf import TNF
from parser import Parser





def VariableListToJSON(num_vars):
    s = "["
    for i in range(num_vars):
        if s!= "[":
            s += ",\"X" + str(i+1) + "\""
        else:
            s += "\"X" + str(i+1) + "\""
    s += "]"

    return s

def countvars(str):
    return sum([c.isnumeric() for c in str])

def count_binops(str):
    return sum([(c == 'v') | (c == '^') for c in str])

def test_rev_polish(str):
    return (len(str) == 0) | (countvars(str) == 1 + count_binops(str))

def do_parens_match(str):
    opens = sum([c == '(' for c in str])
    closes = sum([c == ')' for c in str])
    return opens == closes

NUM_VARS = 10

MIN_WIDTH = 3
MAX_WIDTH = min(10, NUM_VARS)

ROUND_TO = 3

NUM_TEST_CASES = 1000

OUTPUT_TO_FILE = True
DEBUG_ASSIST = False  #Set to True if not outputting JSON

orig_stdout = None
f_out = None

#p_s = [0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.075, 0.075, 0.075, 0.075, 0.075, 0.075, 0.075, 0.075, 0.075, 0.075, 0.075, 0.075]
#p_q = [0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85, 0.95, 0.96, 0.97, 0.98, 0.99, 0.125, 0.175, 0.225, 0.275, 0.325, 0.375, 0.425, 0.475, 0.48, 0.485, 0.49, 0.495]
#p_r = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]

p_s = [0.075, 0.075, 0.075, 0.075, 0.075, 0.075, 0.075, 0.075, 0.075, 0.075, 0.075, 0.075]
p_q = [0.125, 0.175, 0.225, 0.275, 0.325, 0.375, 0.425, 0.475, 0.48, 0.485, 0.49, 0.495]
p_r = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]




test_set_num = 0
for i in range(len(p_s)):
    test_set_num += 1
    if OUTPUT_TO_FILE:
        orig_stdout = sys.stdout
        f_out = open('test_set_' + str(p_s[i]) + '-' + str(p_q[i]) + '-' + str(p_r[i]) + '.json', 'w')
        sys.stdout = f_out
    print("{\"Test Set #\": " + str(test_set_num) + ",")
    print("\"Variables\": " + VariableListToJSON(NUM_VARS) + ",")
    print("\"p_sender\": " + str(p_s[i]) + ",")
    print("\"p_query\": " + str(p_q[i]) + ",")
    print("\"p_receiver\": " + str(round(p_r[i], ROUND_TO)) + ",")
    print("\"Test Cases\": [")
    for j in range(NUM_TEST_CASES):
        print("{\"Test Case #\": " + str(j + 1) + ",")
        sender_truth_set = TruthSet(num_vars=NUM_VARS)
        receiver_truth_set = TruthSet(num_vars=NUM_VARS)
        query_truth_set = TruthSet(num_vars=NUM_VARS)

        for k in range(pow(2, NUM_VARS)):
            r = random.random()
            if r <= p_r[i]:
                receiver_truth_set.add(k)
                if r <= p_q[i]:
                    query_truth_set.add(k)
                    if r <= p_s[i]:
                        sender_truth_set.add(k)

        sender_false_set = sender_truth_set.getComplement()
        receiver_false_set = receiver_truth_set.getComplement()
        query_false_set = query_truth_set.getComplement()

        #rcvr_informed_false_set = receiver_truth_set.getSetDiff(query_truth_set)
        rcvr_informed_false_set = query_false_set.getSetDiff(receiver_false_set)

        sender_tnf = TNF(trueSet=sender_truth_set)
        sender_tnf_postfix = Parser(sender_tnf._tnf).toPostfix(terseness=Parser.ULTRA_TERSE)
        neg_sender_tnf = TNF(trueSet=None, falseSet=sender_false_set)
        neg_sender_tnf_postfix = Parser(neg_sender_tnf._tnf).toPostfix(terseness=Parser.ULTRA_TERSE)
        if len(neg_sender_tnf_postfix) < len(sender_tnf_postfix):
            sender_tnf_postfix = neg_sender_tnf_postfix

        #sender_cnf = CNF.TightCNFFromTruthSet(sender_truth_set)
        sender_cnf = CNF.BuildRandomWidthCNFWithGivenTruthSet(truth_set=sender_truth_set, min_width=MIN_WIDTH,
                                                 max_width=MAX_WIDTH)
        sender_cnf_string = sender_cnf.toString()
        sender_cnf_postfix = Parser(sender_cnf_string).toPostfix(terseness=Parser.ULTRA_TERSE)

        if not test_rev_polish(sender_tnf_postfix):
            print ("PROBLEM WITH sender_tnf!!")
            exit(1)
        if not DEBUG_ASSIST:
            print("\"Sender TNF\": ")
        else:
            print("Sender TNF: (# Zeroes = " + str(len(sender_truth_set._set)) + ")")
        print("\"" + sender_tnf_postfix + "\",")
        if not test_rev_polish(sender_cnf_postfix):
            print ("PROBLEM WITH sender_cnf!!")
            exit(1)
        print("\"Sender CNF\": ")
        print("\"" + sender_cnf_postfix + "\",")
        print("\"Sender Zeroes\": ")
        print(sender_truth_set.toJSON() + ",")

        #query_cnf = CNF.BuildRandomWidthCNFWithGivenTruthSet(truth_set=query_truth_set, min_width=MIN_WIDTH,
        #                                                     max_width=MAX_WIDTH)
        query_tnf = TNF(trueSet=query_truth_set)
        query_tnf_postfix = Parser(query_tnf._tnf).toPostfix(terseness=Parser.ULTRA_TERSE)
        neg_query_tnf = TNF(trueSet=None, falseSet=query_false_set)
        neg_query_tnf_postfix = Parser(neg_query_tnf._tnf).toPostfix(terseness=Parser.ULTRA_TERSE)
        if len(neg_query_tnf_postfix) < len(query_tnf_postfix):
            query_tnf_postfix = neg_query_tnf_postfix

        if not test_rev_polish(query_tnf_postfix):
            print ("PROBLEM WITH query_tnf!!")
            exit(1)
        if not DEBUG_ASSIST:
            print("\"Query TNF\": ")
        else:
            print("Query TNF: (# Zeroes = " + str(len(query_truth_set._set)) + ")")
        #print("\"" + query_tnf._tnf + "\",")
        print("\"" + query_tnf_postfix + "\",")
        print("\"Query Zeroes\": ")
        print(query_truth_set.toJSON() + ",")

        rcvr_informed_query_tnf = TNF(trueSet=None, falseSet=rcvr_informed_false_set)
        rcvr_informed_query_tnf_postfix = Parser(rcvr_informed_query_tnf._tnf).toPostfix(terseness=Parser.ULTRA_TERSE)
        if not test_rev_polish(rcvr_informed_query_tnf_postfix):
            print ("PROBLEM WITH rcvr_informed_query_tnf!!")
            exit(1)
        if not DEBUG_ASSIST:
            print("\"Receiver Informed Query TNF\": ")
        else:
            print("Receiver Informed Query TNF: (# Ones = " + str(len(rcvr_informed_false_set._set)) + ")")
        # print("\"" + rcvr_informed_query_tnf._tnf + "\",")
        print("\"" + rcvr_informed_query_tnf_postfix + "\",")

        #query_cnf = CNF.TightCNFFromTruthSet(query_truth_set)
        query_cnf = CNF.BuildRandomWidthCNFWithGivenTruthSet(truth_set=query_truth_set, min_width=MIN_WIDTH,
                                                              max_width=MAX_WIDTH)
        query_cnf_string = query_cnf.toString()
        query_cnf_postfix = Parser(query_cnf_string).toPostfix(terseness=Parser.ULTRA_TERSE)
        if not test_rev_polish(query_cnf_postfix):
            print ("PROBLEM WITH query_cnf!!")
            exit(1)
        print("\"Query CNF\": ")
        print("\"" + query_cnf_postfix + "\",")

        #receiver_cnf = CNF.BuildRandomWidthCNFWithGivenTruthSet(truth_set=receiver_truth_set, min_width=MIN_WIDTH,
        #                                                        max_width=MAX_WIDTH)
        receiver_tnf = TNF(trueSet=receiver_truth_set)
        receiver_tnf_postfix = Parser(receiver_tnf._tnf).toPostfix(terseness=Parser.ULTRA_TERSE)
        neg_receiver_tnf = TNF(trueSet=None, falseSet=query_false_set)
        neg_receiver_tnf_postfix = Parser(neg_receiver_tnf._tnf).toPostfix(terseness=Parser.ULTRA_TERSE)
        if len(neg_receiver_tnf_postfix) < len(receiver_tnf_postfix):
            receiver_tnf_postfix = neg_receiver_tnf_postfix

        if not test_rev_polish(receiver_tnf_postfix):
            print ("PROBLEM WITH receiver_tnf!!")
            exit(1)
        if not DEBUG_ASSIST:
            print("\"Receiver TNF\": ")
        else:
            print("Receiver TNF: (# Zeroes = " + str(len(receiver_truth_set._set)) + ")")
        #print("\"" + receiver_tnf._tnf + "\",")
        print("\"" + receiver_tnf_postfix + "\",")

        #receiver_cnf = CNF.TightCNFFromTruthSet(receiver_truth_set)
        receiver_cnf = CNF.BuildRandomWidthCNFWithGivenTruthSet(truth_set=receiver_truth_set, min_width=MIN_WIDTH,
                                                             max_width=MAX_WIDTH)
        receiver_cnf_string = receiver_cnf.toString()
        receiver_cnf_postfix = Parser(receiver_cnf_string).toPostfix(terseness=Parser.ULTRA_TERSE)
        if not test_rev_polish(receiver_cnf_postfix):
            print("PROBLEM WITH receiver_cnf!!")
            exit(1)
        print("\"Receiver CNF\": ")
        print("\"" + receiver_cnf_postfix + "\",")

        print("\"Receiver Zeroes\": ")
        print(receiver_truth_set.toJSON())

        if j < NUM_TEST_CASES-1:
            print("},")
        else:
            print("}")

    print("]}")

    if OUTPUT_TO_FILE:
        sys.stdout = orig_stdout
        f_out.close()


