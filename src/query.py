import random
from truthSet import TruthSet

#A Query is just a TruthSet with special properties
class Query(TruthSet):
    def __init__(self, truth_set_s, truth_set_r, distortion=1.0):
        self._distortion = distortion
        #Do initial auditing of input params
        #THIS NEEDS TO BE CHANGED TO USING A BONA FIDE TruthSet!!
        if truth_set_s._num_vars != truth_set_r._num_vars:
            print("Number of variables in the respective truth sets are not compatible! Cannot create Query!")
            return
        if len(truth_set_r._set) < 2*len(truth_set_s._set):
            print("Receiver's truth set must be at least 2X the size of sender's truth set!  Cannot create Query!")
            return

        # First throw in all of S. Then we pick from R \ S in such a way that |R \ Q| is roughly the size of |S|;
        # this is done in addToZeroSet() by passing s_comp and R.
        # It does this by taking elements of R \ S with probability 1 - (|S|/(|R|-|S|)

        s_comp = truth_set_s.getComplement()
        trueSet = self.getInitialTrueSet(r_comp, truth_set_s)
        #print("|Q \ R| = " + str(len(trueSet) - len(truth_set_s._set)) + ", |S| = " + str(len(truth_set_s._set)))


        # Now generate a random probability in p = [.05, .25] and add the points zeros in R \ S into the query
        # with this probability. Compute R \ S via R intersect s_comp

        p = random.uniform(.05, .25)
        s_comp = truth_set_s.getComplement()
        intersection_set = truth_set_r.intersect(s_comp)

        for elem in intersection_set:
            r = random.random()
            if r <= p:
                trueSet.add(elem)

        super().__init__(truth_set_r._num_vars, trueSet)


    def getInitialTrueSet(self, r_comp, s):
        trueSet = set()
        for elem in s._set:
            trueSet.add(elem)

        add_prob = self._distortion * len(s._set) / len(r_comp._set)
        for elem in r_comp._set:
            r = random.random()
            if r <= add_prob:
                trueSet.add(elem)

        return trueSet


    #No longer used
    @classmethod
    def GetRandomSubsetOfSet(cls, set, num_elements_in_subset):
        if num_elements_in_subset > len(set):
            print("num_elements_in_subset is bigger than the number of elements in your set! Cannot return a suitable subset!")
            return None
        #first move the elements in the set to a safe place, in an array (we don't want to touch the original set!)
        arr = []
        for elem in set:
            arr.add(elem)

        subset = set()
        while len(subset) < num_elements_in_subset:
            i = random.randint(0, len(arr) - 1)
            subset.add(arr.pop(i))

        return subset
