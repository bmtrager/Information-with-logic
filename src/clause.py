import random
import math
from truthSet import TruthSet

class Clause:
    def __init__(self, literals, num_vars):
        self._literals = literals
        self._num_vars = num_vars

    @classmethod
    def FromString(cls, num_vars, s_clause):
        literals = Clause.ParseLiteralsFromString(s_clause)
        clause = Clause(literals, num_vars)
        return clause

    @classmethod
    def CreateRandom(cls, num_vars, clause_width=3):
        literals = [0] * clause_width
        if num_vars < clause_width:
            return Clause(literals, num_vars)

        for i in range(clause_width):
            already_present = True
            r = -1
            while already_present:
                r = math.floor(num_vars*random.random()) + 1
                already_present = False
                for j in range(i):
                    if r == abs(literals[j]):
                        already_present = True
                        break
            s = 2*math.floor(2*random.random()) - 1
            literals[i] = s*r
        return Clause(literals, num_vars)

    @classmethod
    def CreateRandomSatisfyingTruthSet(cls, truth_set, min_width, max_width):
        while True:
            interval = max_width - min_width + 1
            random_width = min_width + math.floor(random.random() * interval)
            clause = Clause.CreateRandom(truth_set._num_vars, random_width)
            clause.sortLiterals()
            if clause.satisfiesTruthSet(truth_set):
                return clause

    def sortLiterals(self): #do a post office sort
        sorted_set = [0] * self._num_vars
        for i in range(len(self._literals)):
            sorted_set[abs(self._literals[i])-1] = Clause.Sign(self._literals[i])

        i = 0
        for j in range(self._num_vars):
            if sorted_set[j] != 0:
                self._literals[i] = (j+1)*sorted_set[j]
                i += 1

    @classmethod
    def ParseLiteralsFromString(cls, s_clause):
        literals = []
        tokens = s_clause.split()
        for i in range(len(tokens)):
            where = tokens[i].find('X')
            if where > -1:
                l = 1
                if tokens[i][0] == '-':
                    l = -1
                l *= int(tokens[i][where+1:])
                literals.append(l)

        return literals



    @classmethod
    def Sign(cls, num):
        if num >= 0:
            return 1
        else:
            return -1

    def toString(self, terse=False):
        s = ""
        for i in range(len(self._literals)):
            if i > 0 and not terse:
                s += " v "

            if self._literals[i] < 0:
                s += "-"
            if not terse:
                s += "X" + str(abs(self._literals[i]))
            else:
                s += str(abs(self._literals[i]) - 1)

        return s

    def truthAssignmentSatisfies(self, truthAss):
        assignment_string = TruthSet.ElemToString(truthAss, self._num_vars)
        for literal in self._literals:
            val_string = assignment_string[abs(literal)-1]
            if (literal > 0 and val_string == 'T') or (literal < 0 and val_string == 'F'):
                return True

        return False

    #Must satisfy every truth assignment!
    def satisfiesTruthSet(self, truthSet):
        for truthAss in truthSet._set:
            if not self.truthAssignmentSatisfies(truthAss):
                return False

        return True
