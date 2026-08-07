import math
import random

from truthSet import TruthSet

class TNF:
    def __init__(self, trueSet=None, falseSet=None, inner_tnf=False):  #Only one of trueSet and falseSet should be passed (they should both be of type TruthSet)
        self._trueSet = trueSet
        self._falseSet = falseSet  #yes, it is a bit wierd but the falseSet is a TruthSet!
        self._tnf = self.toString(highest_level=not inner_tnf)
        #self.parenCheck()

    def toString(self, highest_level=True):
        if self._trueSet is None:
            return self.toStringFromFalseSet(highest_level)

        if len(self._trueSet._set) == pow(2, self._trueSet._num_vars): #We are a tautology!!
            return ""

        if len(self._trueSet._set) == 0: #this can only happen at the highest level; return the simplest contradiction
            return self._trueSet._var_labels[0] + " ^ -" + self._trueSet._var_labels[0]

        reducedTrueSet = self._trueSet.copy()
        res = reducedTrueSet.removeConstants()
        if reducedTrueSet._num_vars == 0 or len(reducedTrueSet._set) == pow(2, reducedTrueSet._num_vars):
            return res

        needParensAroundDisjuncts = not highest_level
        if res != "":
            res += " ^ "
            needParensAroundDisjuncts = True

        var, value = reducedTrueSet.getMostBalancedVarAndValue()

        if needParensAroundDisjuncts:  #to go around the big disjunct
            res += '('

        newPosTruthSet = reducedTrueSet.getPositiveReducedSubset(var)
        newPosTNF = TNF(newPosTruthSet, inner_tnf=True)
        newNegTruthSet = reducedTrueSet.getNegativeReducedSubset(var)
        newNegTNF = TNF(newNegTruthSet, inner_tnf=True)
        if newPosTNF._tnf != "":
            res += '('
        res += reducedTrueSet._var_labels[var]
        if newPosTNF._tnf != "":
            res += " ^ "
        #if not TNF.IsAllPositive(newPosTNF._tnf):
        if not TNF.StartsWithConstants(newPosTNF._tnf):
            res = res + "(" + newPosTNF._tnf + ")"
        else:
            res += newPosTNF._tnf
        if newPosTNF._tnf != "":
            res += ')'

        res += " v "

        if newNegTNF._tnf != "":
            res += '('
        res = res + '-' + reducedTrueSet._var_labels[var]
        if newNegTNF._tnf != "":
            res += " ^ "
        #if not TNF.IsAllPositive(newNegTNF._tnf):
        if not TNF.StartsWithConstants(newNegTNF._tnf):
            res = res + "(" + newNegTNF._tnf + ")"
        else:
            res += newNegTNF._tnf
        if newNegTNF._tnf != "":
            res += ')'

        if needParensAroundDisjuncts:   #to end the big disjunct
            res += ')'


        return res

    def toStringFromFalseSet(self, highest_level=True):
        rev_tnf = TNF(trueSet = self._falseSet)
        rev_string = rev_tnf.toString(highest_level=highest_level)
        return "-(" + rev_string + ")"

    @classmethod
    def IsAllPositive(cls, boolExp):
        for i in range(len(boolExp)):
            if boolExp[i] == 'v':
                return False

        return True

    @classmethod
    def StartsWithConstants(cls, boolExp):
        for i in range(len(boolExp)):
            if boolExp[i] == '(':
                return False
            elif boolExp[i] == '^':
                return True
            elif boolExp[i] == 'v':
                return False
        #the case of a single constant
        return True

    #Just used for debugging
    def parenCheck(self):
        pCount = 0
        for i in range(len(self._tnf)):
            if self._tnf[i] == '(':
                pCount += 1
            elif self._tnf[i] == ')':
                pCount -= 1

        if pCount == 0:
            print("parenCheck Success!")
            return True
        else:
            print("parenCheck FAIILURE!!!")
            return False





