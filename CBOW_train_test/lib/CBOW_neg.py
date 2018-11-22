import numpy as np
import random

EXP_TABLE_SIZE = 1000
MAX_EXP = 6

class CBOW:
    def __init__(self, sentence, minCount = 1, vecLength = 200, window = 5):
        self.sentence = sentence
        self.minCount = minCount
        self.vecLength = vecLength
        self.window = window
        self.startingEda = 0.025
        self.round = 1
        self.train_words = 0
        self.tableSize = 1e8
        self.table = []
        self.power = 0.75
        self.neg = 5
        self.vacabSize = 0
        self.trainWordList = []
        self.wordPosiDict = {}
        self.wordPosiList = []
        self.wordVecDict = {}
        self.wordThetaDict = {}
        self.train()

    def train(self):
        eda = self.startingEda
        self.buildWordList()
        print "build word list", len(self.trainWordList), " in all ", len(self.wordVecDict), " after delete min words ", self.train_words, " train words"
        self.initUnigramTable()
        print "generate unigram table"
        word_count = 0
        last_word_count = 0
        word_count_actual = 0
        n = 0
        while n < self.round:
            print "[training] round #" + str(n)
            for i in range(len(self.trainWordList)):
                if self.trainWordList[i] in self.wordVecDict:
                    if word_count - last_word_count > 10000:
                        word_count_actual += (word_count - last_word_count)
                        last_word_count = word_count
                        eda = self.startingEda * (1 - float(word_count_actual) / (self.round * self.train_words + 1))
                        if eda < self.startingEda * 0.0001:
                            eda = self.startingEda * 0.0001
                        print "[training] No." + str(i) + " word as center", len(self.trainWordList), "in all, eda = ", eda
                    self.train1word(i, eda)
                    word_count += 1
            n += 1

    def train1word(self, index, eda):
        w = self.computeW(index)
        if w is None:
            return
        e = np.zeros(self.vecLength)
        for d in range(self.neg + 1):
            targetWord = ""
            if d == 0:
                #positive samlpe
                targetWord = self.trainWordList[index]
                label = 1
            else:
                ran = random.randint(0, self.tableSize - 1)
                # print ran, len(self.table), self.table[ran], len(self.wordPosiList)
                targetWord = self.wordPosiList[self.table[ran]][0]
                label = 0
            f = w.dot(self.wordThetaDict[targetWord])
            if f > MAX_EXP:
                g = (label - 1) * eda
            elif f < -MAX_EXP:
                g = (label - 0) * eda
            else:
                g = (label - self.sig((f + MAX_EXP) * (EXP_TABLE_SIZE / MAX_EXP / 2))) * eda
            e += g * self.wordThetaDict[targetWord]
            self.wordThetaDict[targetWord] += g * w

        for i in range(1, self.window):
            if index + i < len(self.trainWordList):
                word = self.trainWordList[index + i]
                if word in self.wordVecDict:
                    self.wordVecDict[word] = self.wordVecDict[word] + e

            if index - i >= 0:
                word = self.trainWordList[index - i]
                if word in self.wordVecDict:
                    self.wordVecDict[word] = self.wordVecDict[word] + e

    def computeW(self, index):
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
            return None
        w /= tempNum
        return w

    def sig(self, x):
        # print "x: ", x
        tempExp = np.exp((x / EXP_TABLE_SIZE * 2 - 1) * MAX_EXP)
        return tempExp / (tempExp + 1)

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
        self.wordPosiList = list(self.wordPosiDict.items())

        for key, value in self.wordPosiDict.items():
            self.train_words += value

        for word in self.wordPosiDict:
            self.wordVecDict[word] = (np.random.rand(self.vecLength) - np.ones(self.vecLength) * 0.5) / self.vecLength
            self.wordThetaDict[word] = (np.random.rand(self.vecLength) - np.ones(self.vecLength) * 0.5) / self.vecLength

        self.vocabSize = len(self.wordVecDict)

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

    def initUnigramTable(self):
        powSum = 0
        for pair in self.wordPosiList:
            powSum += pair[1] ** self.power
        i = 0
        dl = (self.wordPosiList[i][1] ** self.power) / powSum
        a = 0
        while True:
            if a % 1000000 == 0:
                print "[init gram]", a
            self.table.append(i)
            if float(a) / self.tableSize > dl:
                i += 1
                dl += (self.wordPosiList[i][1] ** self.power) / powSum
            if i >= self.vocabSize:
                i = self.vocabSize - 1
            a += 1
            if a >= self.tableSize:
                break
