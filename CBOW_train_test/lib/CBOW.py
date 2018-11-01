import build_tree as tree
import numpy as np

class CBOW:
    def __init__(self, sentence, minCount = 1, vecLength = 100, window = 5):
        self.sentence = sentence
        self.minCount = minCount
        self.vecLength = vecLength
        self.window = window
        self.eda = 0.025
        self.trainWordList = []
        self.wordPosiDict = {}
        self.wordVecDict = {}
        self.round = 1
        # self.a = 10
        self.train()

    def train(self):
        self.buildWordList()
        print "built word list", len(self.trainWordList), " in all ", len(self.wordVecDict), " after delete min words"
        self.buildTree()
        print "built huffman tree"
        n = 0
        while n < self.round:
            # print self.wordVecDict["limited"]
            print "[training] round #" + str(n)
            maxLoss = 0
            count = 0
            for i in range(len(self.trainWordList)):
                if self.trainWordList[i] in self.wordVecDict:
                    if i % 100 == 0:
                        print "[training] No." + str(i) + " word as center", len(self.trainWordList), "in all"
                    loss = self.train1word(i)
                    if (loss > maxLoss):
                        maxLoss = loss
                    if (loss > 0.04):
                        count += 1
            # print "round" + str(n) + ": " + "max loss: ", maxLoss, "count: ", count
            n += 1

    def train1word(self, index):
        w = np.zeros(self.vecLength)
        tempNum = 0;
        for i in range(1, self.window):
            if index + i < len(self.trainWordList):
                word = self.trainWordList[index + i]
                if word in self.wordVecDict:
                    w = w + self.wordVecDict[word]
                    tempNum += 1
            if index - i >= 0:
                word = self.trainWordList[index - i]
                if word in self.wordVecDict:
                    w = w + self.wordVecDict[word]
                    tempNum += 1
        if tempNum == 0:
            return 0
        w /= tempNum

        e = np.zeros(self.vecLength)
        code = self.tree.wordCodeDict[self.trainWordList[index]]
        node = self.tree.root
        max_q = 0
        for i in range(len(code)):
            q = self.eda * (1 - int(code[i]) - self.sig(np.inner(w, node.value)))
            # if index == 35:
            #     # print "code: ", code[i], "w: ", w, "nodeValue: ", node.value, "inner: ", np.inner(w, node.value)
            #     print "code: ", code[i], q, "inner: ", np.inner(w, node.value)
            # # print np.inner(w, node.value)
            if q > max_q:
                max_q = q

            if node is None:
                raise RuntimeError("code length not right")
            e = e + q * node.value
            node.value = node.value + q * w
            # print "q: ", q, "e: ", e, "theta: ", node.value

            if code[i] == "0":
                node = node.left
            else:
                node = node.right

        for i in range(1, self.window):
            if index + i < len(self.trainWordList):
                word = self.trainWordList[index + i]
                if word in self.wordVecDict:
                    self.wordVecDict[word] = self.wordVecDict[word] + e
            if index - i >= 0:
                word = self.trainWordList[index - i]
                if word in self.wordVecDict:
                    self.wordVecDict[word] = self.wordVecDict[word] + e
        return max_q

    def sig(self, x):
        # print "x: ", x
        return 1 / (1 + np.exp(-x))

    def buildTree(self):
        self.tree = tree.HuffmanTree(self.wordPosiDict, self.vecLength)

    def buildWordList(self):
        self.trainWordList = self.sentence.split()
        for i in range(len(self.trainWordList)):
            self.trainWordList[i] = self.trainWordList[i].strip()

        for word in self.trainWordList:
            if word in self.wordPosiDict:
                self.wordPosiDict[word] += 1
            else:
                self.wordPosiDict[word] = 1
        self.wordPosiDict = self.deleteMinWords()
        for word in self.wordPosiDict:
            self.wordVecDict[word] = np.random.rand(self.vecLength)

    def deleteMinWords(self):
        temp = sorted(self.wordPosiDict.items(), key = lambda x:x[1], reverse = True)
        i = 0
        while (i < len(temp) and temp[i][1] > self.minCount):
            i += 1
        temp = temp[0:i];
        newDict = {}
        for item in temp:
            newDict[item[0]] = item[1]
        return newDict
