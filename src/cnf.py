import math
import random
from collections import OrderedDict
import numpy as np

from clause import Clause
from truthSet import TruthSet


class CNF:
    def __init__(self, num_vars, num_clauses, min_width, max_width):
        self._num_vars = num_vars
        #self._clause_width = clause_width
        self._clauses = set()
        hashedStrings = set()
        for i in range(num_clauses):
            present_already = True
            while present_already:
                #generate random clause width size between min_width and max_width and send to Clause.CreateRandom()
                interval = max_width - min_width + 1
                random_width = min_width + math.floor(random.random() * interval)
                clause = Clause.CreateRandom(num_vars=num_vars, clause_width=random_width)
                clause.sortLiterals()
                s= clause.toString()
                present_already = s in hashedStrings
                if not present_already:
                    self._clauses.add(clause)
                    hashedStrings.add(s)

    @classmethod
    def TightCNFFromTruthSet(cls, truthSet):
        if truthSet.isAllTrue():
            return CNF(num_vars=truthSet._num_vars, num_clauses=0, min_width=0, max_width=0)
        elif truthSet.isAllFalse():
            clause1 = Clause.FromString(num_vars=truthSet._num_vars, s_clause="X1")
            clause2 = Clause.FromString(num_vars=truthSet._num_vars, s_clause="-X1")
            cnf = CNF(num_vars=truthSet._num_vars, num_clauses=0, min_width=0, max_width=0)
            cnf._clauses = {clause1, clause2}
            return cnf

        smartDict = truthSet.getFalseSetSmartDict()
        keys = list(smartDict.keys())
        #values = list(smartDict.values())
        #sorted_value_index = np.argsort(values)
        #sortedSmartDict = {keys[i]: values[i] for i in sorted_value_index}
        cnf = CNF(num_vars=truthSet._num_vars, num_clauses=0, min_width=1, max_width=truthSet._num_vars)
        #keys = list(sortedSmartDict.keys())

        #first create a parent dictionary
        parentDict = dict()
        for key in keys:
            parentDict.update({key: CNF.GetParents(key)})

        #from parent dictionary, create a child dictionary
        childDict = dict()
        for key in keys:
            parents = parentDict.get(key)
            for parent in parents:
                children = childDict.get(parent)
                if children is None:
                    children = {key}
                else:
                    children.add(key)
                childDict.update({parent: children})

        #Now walk through the keys in reverse order to greedily create the clauses
        #does not yet handle case where false set is all values or empty!!
        deletedSet = set()
        clauses = set()
        for key, value in sorted(smartDict.items(), key=lambda item: item[1], reverse=True):
            if key not in deletedSet:
                countStars = key.count('*')
                if value == pow(2, countStars):
                    clause = CNF.ClauseFromFalseMask(key)
                    clauses.add(clause)
                    children = childDict.get(key)
                    if countStars > 0:
                        deletedSet = deletedSet.union(children)

        cnf._clauses = clauses
        return cnf



    @classmethod
    def ClauseFromFalseMask(cls, mask):
        s = ""
        for i in range(len(mask)):
            if mask[i] != '*':
                if len(s) > 0:
                    s += " v "
                if mask[i] == '1':
                    s += '-'
                s = s + 'X' + str(i+1)

        return Clause.FromString(len(mask), s)




    @classmethod
    def GetParents(cls, s):
        parents = set()
        if s.count('*') < len(s):
            for i in range(len(s)):
                if s[i] != '*':
                    parent = s[0:i] + '*' + s[i+1:]
                    parents.add(parent)
                    parents = parents.union(CNF.GetParents(parent))

        return parents

    #@classmethod
    #def GetChildren(cls, s):  #This method is not needed - should just use the childDict to delete children
    #    children = set()
    #    if s.count('*') > 1:
    #        if s[i] == '*':   #These may or may not be valid children; perhaps important to verify that children are needed
    #            child1 = s[0:i] + '0' + s[i+1:]
    #            child2 = s[0:i] + '1' + s[i + 1:]
    #            if child1 not in children:
    #                children.add(child1)
    #                children.union(CNF.GetChildren(child1))
    #            if child2 not in children:
    #                children.add(child2)
    #                children.union(CNF.GetChildren(child2))
    #
    #    return children





    @classmethod
    def FromString(cls, num_vars, s_cnf):
        clauses = set()
        pending_s_clause = ""
        clause_pending = False
        for ch in s_cnf:
            if clause_pending:
                if ch != ')':
                    pending_s_clause += ch
                else:
                    clause = Clause.FromString(num_vars, pending_s_clause)
                    clauses.add(clause)
                    clause_pending = False
                    pending_s_clause = ""
            else:
                if ch == '(':
                    clause_pending = True

        cnf = CNF(num_vars, num_clauses=0, min_width=0, max_width=0)
        cnf._clauses = clauses
        return cnf


    def getAllTrueAssignments(self):
        truthSet = TruthSet.CreateRandom(self._num_vars, prob=1.0)
        for clause in self._clauses:
            truthSet.update(clause)

        return truthSet

    def toString(self, terse=False):
        s = ""
        for clause in self._clauses:
            if s != "":
                if not terse:
                    s += " ^ "
                else:
                    s += "^"
            if not terse:
                s += "(" + clause.toString() + ")"
            else:
                s += clause.toString(terse=terse)

        return s

    @classmethod
    def BuildFixedWidthCNFCompatibleWithTruthSet(cls, truthSet, num_vars, num_clauses, clause_width = 3):
        cnf = CNF(num_vars, 0, clause_width)
        hashedStrings = set()
        for i in range(num_clauses):
            present_already = True
            while present_already:
                satisfiesTruthSet = False
                clause = None
                while not satisfiesTruthSet:
                    clause = Clause.CreateRandom(num_vars=num_vars, clause_width=clause_width)
                    satisfiesTruthSet = clause.satisfiesTruthSet(truthSet)
                clause.sortLiterals()
                s = clause.toString()
                present_already = s in hashedStrings
                if not present_already:
                    cnf._clauses.add(clause)
                    hashedStrings.add(s)

        return cnf

    @classmethod
    def BuildRandomWidthCNFCompatibleWithTruthSet(cls, truthSet, num_vars, num_clauses, min_width, max_width):
        cnf = CNF(num_vars, 0, min_width, max_width)
        hashedStrings = set()
        for i in range(num_clauses):
            present_already = True
            while present_already:
                satisfiesTruthSet = False
                clause = None
                while not satisfiesTruthSet:
                    interval = max_width - min_width + 1
                    random_width = min_width + math.floor(random.random() * interval)
                    clause = Clause.CreateRandom(num_vars=num_vars, clause_width=random_width)
                    satisfiesTruthSet = clause.satisfiesTruthSet(truthSet)
                clause.sortLiterals()
                s = clause.toString()
                present_already = s in hashedStrings
                if not present_already:
                    cnf._clauses.add(clause)
                    hashedStrings.add(s)

        return cnf

    @classmethod
    def BuildRandomWidthCNFWithGivenTruthSet(cls, truth_set, min_width, max_width):
        truth_set_clone = truth_set.clone()  #important to use a clone since we remove elements from the truth set, thus destroying it!!
        cnf = CNF(truth_set_clone._num_vars, 0, min_width, max_width)
        hashedStrings = set()
        num_zeroes_in_truth_set = len(truth_set_clone._set)  #to make sure we stop when we reduce our truth set to this size
        our_truth_set_so_far = TruthSet.CreateRandom(truth_set_clone._num_vars, prob=1.0)
        num_zeros_in_truth_set_so_far = len(our_truth_set_so_far._set)
        #print("Target # of zeros: " + str(num_zeroes_in_truth_set))
        #print("# zeros to start: " + str(num_zeros_in_truth_set_so_far))
        while num_zeros_in_truth_set_so_far > num_zeroes_in_truth_set:
            clause = Clause.CreateRandomSatisfyingTruthSet(truth_set_clone, min_width, max_width)
            our_truth_set_so_far.update(clause)
            if len(our_truth_set_so_far._set) < num_zeros_in_truth_set_so_far:
                num_zeros_in_truth_set_so_far = len(our_truth_set_so_far._set)
                #print("# zeros updated to: " + str(num_zeros_in_truth_set_so_far))
                clause.sortLiterals()
                cnf._clauses.add(clause)

        return cnf


    def getPercentageOfOverlappinigClauses(self, cnf2):
        hashedClaauseStrings = set()
        numClauses = len(self._clauses)
        for clause in self._clauses:
            hashedClaauseStrings.add(clause.toString())

        numMatches = 0
        for  clause in cnf2._clauses:
            if clause.toString() in hashedClaauseStrings:
                numMatches += 1

        return numMatches/numClauses



