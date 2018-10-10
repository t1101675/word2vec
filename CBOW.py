import build_tree as tree
import numpy as np

class CBOW:
    def __init__(self, sentence, minCount = 1, vecLength = 5, window = 5):
        self.sentence = sentence
        self.minCount = minCount
        self.vecLength = vecLength
        self.window = window
        self.eda = 0.1
        self.trainWordList = []
        self.wordPosiDict = {}
        self.wordVecDict = {}
        self.round = 5
        self.a = 10
        self.train()

    def train(self):
        self.buildWordList()
        self.buildTree()
        n = 0
        while n < self.round:
            # print self.wordVecDict["limited"]
            for i in range(len(self.trainWordList)):
                # print i
                self.train1word(i)
            n += 1

    def train1word(self, index):
        w = np.zeros(self.vecLength)
        for i in range(1, self.window):
            if index + i < len(self.trainWordList):
                word = self.trainWordList[index + i]
                w = w + self.wordVecDict[word]
            if index - i >= 0:
                word = self.trainWordList[index - i]
                w = w + self.wordVecDict[word]

        w /= 2 * self.window
        e = np.zeros(self.vecLength)
        code = self.tree.wordCodeDict[self.trainWordList[index]]
        node = self.tree.root
        for i in range(len(code)):
            q = self.eda * (1 - int(code[i]) - self.sig(w * node.value))
            # print "q: ", q
            if node is None:
                raise RuntimeError("code length not right")
            e = e + q * node.value
            node.value = node.value + q * w
            if code[i] == "0":
                node = node.left
            else:
                node = node.right

        for i in range(1, self.window):
            if index + i < len(self.trainWordList):
                word = self.trainWordList[index + i]
                self.wordVecDict[word] = self.wordVecDict[word] + e
            if index - i >= 0:
                word = self.trainWordList[index - i]
                self.wordVecDict[word] = self.wordVecDict[word] + e

    def sig(self, x):
        # print "x: ", x
        return 1 / (1 + np.exp(-x))

    def buildTree(self):
        self.tree = tree.HuffmanTree(self.wordPosiDict, self.vecLength)

    def buildWordList(self):
        self.trainWordList = self.sentence.split(" ")
        for word in self.trainWordList:
            if word in self.wordPosiDict:
                self.wordPosiDict[word] += 1
            else:
                self.wordPosiDict[word] = 1
                self.wordVecDict[word] = np.random.rand(1, self.vecLength)
