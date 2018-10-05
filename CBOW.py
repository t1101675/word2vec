import build_tree as tree
import numpy as np

class CBOW:
    def __init__(self, sentence, minCount = 1, vecLength = 100, window = 5):
        self.sentence = sentence
        self.minCount = minCount
        self.vecLength = vecLength
        self.window = window
        self.eda = 1
        self.trainWordList = []
        self.wordPosiDict = []
        self.wordVecDict = {}
        self.round = 1

    def train(self):
        buildWordList()
        self.tree = tree.HuffmanTree(self.wordList, self.vecLength)
        n = 0
        while n < self.round:
            for i in range(len(trainWordList)):
                train1word(i)

    def train1word(self, index):
        w = np.zeros(self.vecLength)
        for i in range(1, self.window):
            if index + i < len(trainWordList):
                word = trainWordList[index + i]
                w = w + wordVecDict[word]
            if index - i >= 0:
                word = trainWordList[index - i]
                w = w + wordVecDict[word]

        e = np.zeros(self.vecLength)
        code = self.tree.wordCodeDict[trainWordList[index]]
        node = self.tree.root
        q = eda * (1 - int(code[i]) - sig(w * node.value))
        for i in range(len(code)):
            if node is None:
                raise RuntimeError("code length not right")
            node.value = node.value + q * w
            e = e + q * node.value
            if code[i] == "0":
                node = node.left
            else:
                node = node.right

    def sig(x):
        return 1 / (1 + exp(-x))

    def buildWordList():
        trainWordList = sentence.split(" ")
        for word in trainWordList:
            if word in wordPosiDict:
                wordPosiDict[word] += 1
            else:
                wordPosiDict[word] = 1
                wordVecDict[word] = np.random.rand(1, self.vecLength)


                
