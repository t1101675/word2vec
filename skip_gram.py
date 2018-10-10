import build_tree as tree
import numpy as np

class SkipGram:
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
            maxLoss = 0
            for i in range(len(self.trainWordList)):
                loss = self.train1word(i)
                if loss > maxLoss:
                    maxLoss = loss
            print "round" + str(n) + ": " + "max loss: ", maxLoss
            n += 1

    def train1word(self, index):
        nearWords = []
        for i in range(1, self.window):
            if index + i < len(self.trainWordList):
                nearWords.append(self.trainWordList[index + i])
            if index - i >= 0:
                nearWords.append(self.trainWordList[index - i])

        max_q = 0
        for word in nearWords:
            wordVec = self.wordVecDict[word]
            e = np.zeros(self.vecLength)
            code = self.tree.wordCodeDict[self.trainWordList[index]]
            node = self.tree.root
            for i in range(len(code)):
                q = self.eda * (1 - int(code[i]) - self.sig(np.inner(wordVec, node.value)))
                if index == 0:
                    print "code: ", code[i], q, "inner: ", np.inner(wordVec, node.value)

                # print q
                if q > max_q:
                    max_q = q

                if node is None:
                    raise RuntimeError("code length not right")
                e = e * q * node.value
                node.value = node.value + q * wordVec

                if code[i] == "0":
                    node = node.left
                else:
                    node = node.right

            self.wordVecDict[word] += e
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
