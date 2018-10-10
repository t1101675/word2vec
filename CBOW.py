import build_tree as tree
import numpy as np

class CBOW:
    def __init__(self, sentence, minCount = 1, vecLength = 20, window = 5):
        self.sentence = sentence
        self.minCount = minCount
        self.vecLength = vecLength
        self.window = window
        self.eda = 0.05
        self.trainWordList = []
        self.wordPosiDict = {}
        self.wordVecDict = {}
        self.round = 100
        self.a = 10
        self.train()

    def train(self):
        self.buildWordList()
        print "built word list", len(self.trainWordList), " in all"
        self.buildTree()
        print "built huffman tree"
        n = 0
        while n < self.round:
            print self.wordVecDict["limited"]
            maxLoss = 0
            count = 0
            for i in range(len(self.trainWordList)):
                # print i
                loss = self.train1word(i)
                if (loss > maxLoss):
                    maxLoss = loss
                if (loss > 0.04):
                    count += 1
            print "round" + str(n) + ": " + "max loss: ", maxLoss, "count: ", count
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
        max_q = 0
        for i in range(len(code)):
            q = self.eda * (1 - int(code[i]) - self.sig(np.inner(w, node.value)))
            if index == 35:
                # print "code: ", code[i], "w: ", w, "nodeValue: ", node.value, "inner: ", np.inner(w, node.value)
                print "code: ", code[i], q, "inner: ", np.inner(w, node.value)
            # print np.inner(w, node.value)
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
                self.wordVecDict[word] = self.wordVecDict[word] + e
            if index - i >= 0:
                word = self.trainWordList[index - i]
                self.wordVecDict[word] = self.wordVecDict[word] + e
        return max_q

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
