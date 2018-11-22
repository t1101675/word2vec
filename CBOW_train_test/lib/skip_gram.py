import build_tree as tree
import numpy as np

TABLE_SIZE = 1000
EXP = 6

class SkipGram:
    def __init__(self, sentence, minCount = 1, vecLength = 20, window = 5):
        self.sentence = sentence
        self.minCount = minCount
        self.vecLength = vecLength
        self.window = window
        self.startingEda = 0.025
        self.trainWordList = []
        self.wordPosiDict = {}
        self.wordVecDict = {}
        self.round = 1
        self.train_words = 0
        self.train()

    def train(self):
        self.buildWordList()
        print "built word list", len(self.trainWordList), " in all ", len(self.wordVecDict), " after delete min words ", self.train_words, " train words"
        self.buildTree()
        print "built huffman tree"
        n = 0
        word_count = 0
        last_word_count = 0
        word_count_actual = 0
        while n < self.round:
            print "[training] round #" + str(n)
            for i in range(len(self.trainWordList)):
                if self.trainWordList[i] in self.wordVecDict:
                    if word_count - last_word_count > 10000:
                        word_count_actual += (word_count - last_word_count)
                        last_word_count = word_count
                        eda = self.startingEda * (1 - float(word_count_actual) / (self.round * self.train_words + 1))
                        if (eda < self.startingEda * 0.0001):
                            eda = self.startingEda * 0.0001
                        print "[training] No." + str(i) + " word as center", len(self.trainWordList), "in all, eda = ", eda

                    self.train1word(i, eda)
            n += 1

    def train1word(self, index, eda):
        nearWords = []
        for i in range(1, self.window):
            if index + i < len(self.trainWordList):
                nearWords.append(self.trainWordList[index + i])
            if index - i >= 0:
                nearWords.append(self.trainWordList[index - i])

        for word in nearWords:
            wordVec = self.wordVecDict[word]
            e = np.zeros(self.vecLength)
            code = self.tree.wordCodeDict[self.trainWordList[index]]
            node = self.tree.root
            for i in range(len(code)):
                f = wordVec.dot(node.value)
                if f <= -MAX_EXP:
                    continue
                elif f >= MAX_EXP:
                    continue
                else:
                    f = self.sig((f + MAX_EXP) * (EXP_TABLE_SIZE / MAX_EXP / 2))
                q = eda * (1 - int(code[i]) - f)

                if node is None:
                    raise RuntimeError("code length not right")
                e = e + q * node.value
                node.value = node.value + q * wordVec

                if code[i] == "0":
                    node = node.left
                else:
                    node = node.right

            self.wordVecDict[word] += e

    def sig(self, x):
        # print "x: ", x
        tempExp = np.exp((x / EXP_TABLE_SIZE * 2 - 1) * MAX_EXP)
        return tempExp / (tempExp + 1)

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

        for key, value in self.wordPosiDict.items():
            self.train_words += value

        for word in self.wordPosiDict:
            self.wordVecDict[word] = (np.random.rand(self.vecLength) - np.ones(self.vecLength) * 0.5) / self.vecLength;

    def deleteMinWords(self):
        temp = sorted(self.wordPosiDict.items(), key = lambda x:x[1], reverse = True)
        i = 0
        while (i < len(temp) and temp[i][1] >= self.minCount):
            i += 1
        temp = temp[0:i];
        newDict = {}
        for item in temp:
            newDict[item[0]] = item[1]
        return newDict
