import clause
import random

class TruthSet:
    POSITIVE = 1
    NEGATIVE = 0

    def __init__(self, num_vars, truth_set=None):
        self._num_vars = num_vars
        if truth_set != None:
            self._set = truth_set
        else:
            self._set = set()
        self._var_labels = [""] * num_vars
        self.setDefaultLabels()

    def copy(self):
        truthSetCopy = TruthSet(num_vars=self._num_vars, truth_set=self._set.copy())
        truthSetCopy.setLabels(self._var_labels)
        return truthSetCopy

    #for constructing a random TruthSet
    @classmethod
    def CreateRandom(cls, num_vars, prob=1):
        trueSet = set()
        for i in range(pow(2, num_vars)):
            r = random.random()
            if r < prob:
                trueSet.add(i)
        return TruthSet(num_vars, trueSet)

    def setDefaultLabels(self):
        self._var_labels = [""] * self._num_vars
        for i in range(self._num_vars):
            self._var_labels[i] = "X" + str(i+1)

    def setLabels(self, labels):
        if len(labels) != self._num_vars:
            print("Number of labels does not match number of variables! Cannot set labels!")
        else:
            for i in range(self._num_vars):
                self._var_labels[i] = labels[i]

    def addToSet(self, prob):
        for i in range(pow(2, self._num_vars)):
            if i not in self._set:
                r = random.random()
                if r < prob:
                    self._set.add(i)

    def update(self, clause):
        elemsToRemove = set()
        for elem in self._set:
            #print("Clause: " + clause.toString())
            #print("Truth assignment = " + TruthSet.ElemToString(elem,self._num_vars))
            if not clause.truthAssignmentSatisfies(elem):
                #print("Not satisfied!")
                elemsToRemove.add(elem)
            #else:
                #print("Satisfied!")
        for elem in elemsToRemove:
            self._set.remove(elem)

    def add(self, elem):
        self._set.add(elem)

    def remove(self, elem):
        self._set.remove(elem)

    def isAllTrue(self):
        return len(self._set) == pow(2, self._num_vars)

    def isAllFalse(self):
        return self.isEmpty()

    def isEmpty(self):
        return len(self._set) == 0

    def getComplement(self):
        complement = set()
        in_array = [0] * (2**self._num_vars)
        for elem in self._set:
            in_array[elem] = 1

        for i in range(len(in_array)):
            if in_array[i] == 0:
                complement.add(i)

        return TruthSet(self._num_vars, complement)

    def getSetDiff(self, truth_set):  #return truth set corresponding to this \ truth_set
        diff_set = self._set.copy() - truth_set._set
        return TruthSet(self._num_vars, diff_set)

    def intersect(self, truth_set):
        intersection_set = set()
        this_array = [0] * (2**self._num_vars)
        for elem in self._set:
            this_array[elem] = 1

        for elem in truth_set._set:
            if this_array[elem] == 1:
                intersection_set.add(elem)

        return intersection_set

    def equals(self, otherTS):
        if self._num_vars != otherTS._num_vars:
            print("Number of variables do not match! Truth Sets cannot possibly match!")
            return False

        if len(self._set) != len(otherTS._set):
            print("Truth Sets are of different sizes so cannot possibly match!")
            print("This truth set size = " + str(len(self._set)))
            print("Other truth set size = " + str(len(otherTS._set)))
            return False

        for elem in self._set:
            if elem not in otherTS._set:
                return False
        for elem in otherTS._set:
            if elem not in self._set:
                return False

        return True

    def clone(self):
        clonedTS = TruthSet(0)
        clonedTS._set = set()
        clonedTS._num_vars = self._num_vars
        clonedTS._var_labels = self._var_labels
        for elem in self._set:
            clonedTS._set.add(elem)
        return clonedTS

    @classmethod
    def FromString(cls, s_truth_set, trueChar="1", falseChar="0"):
        tset = set()
        elem_pending = False
        elem_so_far = ""
        num_vars = 0
        for ch in s_truth_set:
            if elem_pending:
                if ch != '"':
                    elem_so_far += ch
                else:
                    num_vars = len(elem_so_far)
                    elem = TruthSet.StringToElem(elem_so_far, num_vars=num_vars, trueChar=trueChar, falseChar=falseChar)
                    tset.add(elem)
                    elem_pending = False
                    elem_so_far = ""

        truthSet = TruthSet(num_vars=num_vars)
        truthSet._set = tset
        return truthSet

    @classmethod
    def FromArrayOfStrings(cls, a_truth_set, trueChar="1", falseChar="0"):
        tset = set()
        num_vars = 0
        if len(a_truth_set) > 0:
            num_vars = len(a_truth_set[0])
        for s in a_truth_set:
            elem = TruthSet.StringToElem(s, num_vars=num_vars, trueChar=trueChar, falseChar=falseChar)
            tset.add(elem)

        truthSet = TruthSet(num_vars=num_vars)
        truthSet._set = tset
        return truthSet


    def toString(self, trueChar="1", falseChar="0"):
        s = ""
        for elem in self._set:
            s += TruthSet.ElemToString(elem, self._num_vars, trueChar=trueChar, falseChar=falseChar) + "\n"

        return s

    def getFalseSetSmartDict(self):
        falseSet = self.getComplement();
        smartDict = dict()
        smartDictMaskList = []
        for i in range(1, pow(2, self._num_vars)):
            s = TruthSet.ElemToString(i, self._num_vars, trueChar="1", falseChar="0")
            smartDictMaskList.append(s)
            #smartDictMasklist.append({s: s.count('1')})

        for elem in falseSet._set:
            s = TruthSet.ElemToString(elem, falseSet._num_vars, trueChar="1", falseChar="0")
            falseSet.toDict(s, smartDict, smartDictMaskList)

        return smartDict

    def toDict(self, s, smartDict, smartDictMaskList):
        smartDict.update({s: 1})
        for i in range(len(smartDictMaskList)):
            s_masked = ""
            for j in range(self._num_vars):
                if smartDictMaskList[i][j] == '1':
                    s_masked += '*'
                else:
                    s_masked += s[j]
            count = smartDict.get(s_masked)
            if count == None:
                smartDict.update({s_masked: 1})
            else:
                smartDict.update({s_masked: count + 1})


    def toJSON(self):
        if len(self._set) == 0:
            return "[]"

        s = "["
        for elem in self._set:
            s += "\"" + TruthSet.ElemToString(elem, self._num_vars, trueChar="1", falseChar="0") + "\",\n"

        s = s[0:len(s) - 2] + "]"
        return s

    def getBalancesByVar(self):
        balances = [0]*self._num_vars
        for i in range(len(balances)):
            balances[i] = 0
            for elem in self._set:
                if self.isElemPositiveForVar(elem, i):
                    balances[i] += 1
                else:
                    balances[i] -= 1

        return balances

    def isElemPositiveForVar(self, elem, var):
        elem_string = TruthSet.ElemToString(elem, self._num_vars, trueChar="1", falseChar="0")
        return elem_string[var] == '1'

    def getMostBalancedVarAndValue(self):
        balances = self.getBalancesByVar()
        mostBalancedVar = -1
        closestBalance = 999
        for i in range(len(balances)):
            if abs(balances[i]) < abs(closestBalance):
                mostBalancedVar = i
                closestBalance = balances[i]

        return mostBalancedVar, closestBalance

    def getBalancesByVarAsString(self):
        balances = self.getBalancesByVar()
        res = ""
        for i in range(len(balances)):
            res = res + self._var_labels[i] + ": "
            if balances[i] > 0:
                res += '+'
            res += str(balances[i])
            if i < len(balances) - 1:
                res += ", "

        return res

    def getPositiveReducedSubset(self, var):
        return self.getReducedTruthSet(var, TruthSet.POSITIVE)

    def getNegativeReducedSubset(self, var):
        return self.getReducedTruthSet(var, TruthSet.NEGATIVE)

    def getReducedTruthSet(self, var, polarity):
        reducedSubset = set()
        for elem in self._set:
            isElemPositive = self.isElemPositiveForVar(elem, var)
            if (isElemPositive and polarity == TruthSet.POSITIVE) or \
                    (not isElemPositive and polarity == TruthSet.NEGATIVE):
                reducedElem = TruthSet.GetReducedElem(elem, self._num_vars, var)
                reducedSubset.add(reducedElem)

        newVarLabels = self.getReducedVarLabels(var)
        reducedTruthSet = TruthSet(self._num_vars-1, reducedSubset)
        reducedTruthSet.setLabels(newVarLabels)
        return reducedTruthSet

    #returns the constant string description
    def removeConstants(self):
        num_non_constants = 0
        constants = [True] * self._num_vars
        first_string = ""
        first_elem = True
        for elem in self._set:
            s = TruthSet.ElemToString(elem, self._num_vars)
            if not first_elem:
                for i in range(self._num_vars):
                    if constants[i] and s[i] != first_string[i]:
                        constants[i] = False
                        num_non_constants += 1
                        if num_non_constants == self._num_vars:
                            return ""
            else:
                first_string = s
                first_elem = False

        constants_str = ""
        newVarLabels = []
        for i in range(self._num_vars):
            if constants[i]:
                if constants_str != "":
                    constants_str += " ^ "
                if first_string[i] == 'F':
                    constants_str += '-'
                constants_str += self._var_labels[i]
            else:
                newVarLabels.append(self._var_labels[i])

        newSet = set()
        for elem in self._set:
            s = TruthSet.ElemToString(elem, self._num_vars)
            reduced_s = ""
            for i in range(self._num_vars):
                if not constants[i]:
                    reduced_s += s[i]
            new_elem = 0
            for i in range(num_non_constants):
                if reduced_s[i] == "T":
                    new_elem += pow(2, num_non_constants - i - 1)
            newSet.add(new_elem)

        self._num_vars = num_non_constants
        self._set = newSet
        self._var_labels = newVarLabels
        return constants_str

    def getReducedVarLabels(self, var):
        #print("Var labels before:" + str(self._var_labels))
        #print("var = " + str(var))
        newVarLabels = [""] * (self._num_vars - 1)
        for i in range(var):
            newVarLabels[i] = self._var_labels[i]
        for i in range(var + 1, self._num_vars):
            newVarLabels[i - 1] = self._var_labels[i]

        #print("Var labels after:" + str(newVarLabels))
        return newVarLabels

    @classmethod
    def ElemToString(cls, elem, num_vars, trueChar="T", falseChar="F"):
        if num_vars == 0:
            return ""

        s = ""
        if elem >= pow(2, num_vars - 1):
            elem -= pow(2, num_vars - 1)
            s += trueChar + TruthSet.ElemToString(elem, num_vars-1, trueChar, falseChar)
        else:
            s += falseChar + TruthSet.ElemToString(elem, num_vars - 1, trueChar, falseChar)

        return s

    @classmethod
    def StringToElem(cls, str, num_vars, trueChar="T", falseChar="F"):
        elem = 0
        for i in range(len(str)):
            if str[i] == trueChar:
                elem += pow(2, num_vars-i-1)

        return elem

    @classmethod
    def GetReducedElem(cls, elem, num_vars, var_to_eliminate):
        s = TruthSet.ElemToString(elem, num_vars)
        reducedStr = s[0:var_to_eliminate] + s[var_to_eliminate+1:]
        return TruthSet.StringToElem(reducedStr, num_vars-1)
