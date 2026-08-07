import re

class Block:
    def __init__(self, blockNum, beginPos, endPos, text):
        self._blockNum = blockNum
        self._beginPos = beginPos
        self._endPos = endPos
        self._text = text

    def toString(self):
        res = "Block num: " + str(self._blockNum) + "\n"
        res = res + "Begin pos: " + str(self._beginPos) + "\n"
        res = res + "End pos: " + str(self._endPos) + "\n"
        res = res + "Text: \"" + self._text + "\"\n"
        res = res + "Postfix: " + self.postFix() + "\n"
        return res

    def suckSpaces(self):
        res = ""
        for i in range(len(self._text)):
            ch = self._text[i]
            if ch != ' ':
                res += ch
        self._text = res

    def postFix(self):
        #self.suckSpaces()
        vList = Block.GetOrderedVariableList(self._text)

        if len(vList) == 1:
            #print("IN: " + self._text)
            #print("OUT: " +  vList[0])
            return vList[0]

        con = Block.GetConnective(self._text)
        w_con = ' ' + con + ' '
        pf = vList[0] + " " + vList[1] + w_con

        for i in range(2, len(vList)):
            pf += vList[i] + w_con

        #print("IN: " + self._text)
        #print("OUT: " + pf)
        return pf

    @classmethod
    def GetOrderedVariableList(cls, s):
        vList = []
        varPending = False
        varStartPos = -1
        for i in range(len(s)):
            ch = s[i]
            if ch == 'X' or ch == 'B' or ch == '-' or ('0' <= ch and ch <= '9'):
                if not varPending:
                    varStartPos = i
                    varPending = True
            else:
                if varPending:
                    vList.append(s[varStartPos:i])
                    varPending = False
                    varStartPos = -1

        if varPending:
            vList.append(s[varStartPos:])

        return vList

    @classmethod
    def GetConnective(cls, s):
        for ch in s:
            if ch == 'v' or ch == '^':
                return ch

        return ""

class Parser:
    # terseness settings when performing  postfix
    EASILY_READABLE = -1
    TERSE = -2 #remove "X"s from variable names
    ULTRA_TERSE = -3 #also shift  1-10 to 0-9 and remove spacing

    def __init__(self, expression):
        self._expression = expression
        self._blocks = []
        if expression == "":
            self._parse = ""
        else:
            self._parse = self.parse('(' + expression + ')')


    def parse(self, exp):
        e = exp  #work on copy, not the real expression
        openParenLoc = -1
        startingBlockNum = len(self._blocks)
        for i in range(len(e)):
            ch = e[i]
            if ch == '(':
                openParenLoc = i
            elif ch == ')':
                if openParenLoc >= 0:
                    self._blocks.append(Block(len(self._blocks), openParenLoc, i, e[openParenLoc:i+1]))
                    openParenLoc = -1

        for i in range(len(self._blocks)-1, startingBlockNum-1, -1):
            block = self._blocks[i]
            e = e[:block._beginPos] + " B" + str(i) + " " + e[block._endPos + 1:]

        if len(self._blocks) != startingBlockNum:
            return self.parse(e)
        else:
            return e

    @classmethod
    def SmartReplace(cls, startingText, vbl, replacingText):
        locs = [m.start() for m in re.finditer(vbl, startingText)]
        newText = startingText
        maskForNotReplacing = 'N' * len(vbl)
        maskForReplacing = 'R' * len(vbl)
        for loc in locs:
            if loc + len(vbl) < len(startingText):
                ch = startingText[loc + len(vbl)]
                if ch >= '0' and ch <= '9':
                    newText = newText.replace(vbl, maskForNotReplacing, 1)
                else:
                    newText = newText.replace(vbl, maskForReplacing, 1)
            else:
                newText = newText.replace(vbl, maskForReplacing, 1)

        newText = newText.replace(maskForReplacing, replacingText)
        newText = newText.replace(maskForNotReplacing, vbl)
        return newText



    def blockUnwind(self, block):
        orig_block = block._text
        pf = block.postFix()

        vList = Block.GetOrderedVariableList(pf)
        for vbl in vList:
            if vbl[0] == 'B':
                blockNum = int(vbl[1:])
                replacingText = self.blockUnwind(self._blocks[blockNum])
                #print("Block #:" + str(blockNum))
                #print("Replacing text:" + replacingText)
                #pf = pf.replace(vbl, replacingText)
                pf = Parser.SmartReplace(pf, vbl, replacingText)
            elif vbl[0:2] == "-B":
                blockNum = int(vbl[2:])
                replacingText = self.blockUnwind(self._blocks[blockNum])
                #print("Block #:" + str(blockNum))
                #print("Replacing text:" + replacingText)
                #pf = '-' + pf.replace(vbl, replacingText)
                pf = Parser.SmartReplace(pf, vbl, replacingText)
        #print("Block: " + orig_block)
        #print("Unwound block: " + pf)
        return pf

    @classmethod
    def PostfixNegations(cls, pf):  #Assumes negations are applied only to variables or to the entire string (i.e. at the highest level)
        res = ""
        postfixFinalNegation = False
        if pf[0] == '-' and pf[1] == ' ':  #this is sort of cheesy...
            postfixFinalNegation = True
            pf = pf[2:len(pf)]
        i = 0
        while i < len(pf):
            if pf[i] == '-':
                vbleName = Parser.GetVariableStartingAt(pf, i+1)
                res += vbleName + '-'
                i += (len(vbleName) + 1)
            else:
                res += pf[i]
                i += 1

        if postfixFinalNegation:
            res += '-'

        return res

    @classmethod
    def GetVariableStartingAt(cls, pf, startingAt):
        i = startingAt
        while ('0' <= pf[i] <= '9') or ('a' <= pf[i] <= 'z') or ('A' <= pf[i] <= 'Z'):
            i += 1
            if i == len(pf):  #added this check
                break

        endingAt = i
        return pf[startingAt:endingAt]

    def toPostfix(self, terseness=EASILY_READABLE):
        if self._expression == "-()":
            #print("Critical section!")
            return "00-^"
        if len(self._blocks) > 0:
            pf = self.blockUnwind(self._blocks[len(self._blocks) - 1])
            #print("1.pf = " + pf)
            pf = Parser.PostfixNegations(pf)
            #print("2.pf = " + pf)
            if terseness != Parser.EASILY_READABLE:
                pf = pf.replace("X", "")
                #print("3.pf = " + pf)
            if terseness == Parser.ULTRA_TERSE:
                for i in range(0,10):
                    f = str(i+1) + " "
                    t = str(i) + " "
                    pf = pf.replace(f, t)
                    f = str(i + 1) + "-"
                    t = str(i) + "-"
                    pf = pf.replace(f, t)
                pf = pf.replace(" ", "")
            return pf
        else:
            return ""








