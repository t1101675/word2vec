import build_tree as tree
import numpy as np

EXP_TABLE_SIZE = 1000
MAX_EXP = 6

class Word2Vec:
    def __init__(self, sentence, minCount = 5, vecLength = 200, window = 8, iter = 1, eda = 0.025):
        self.sentence = sentence
        self.minCount = minCount
        self.vecLength = vecLength
        self.window = window
        self.iter = iter
        self.startingEda = eda
        self.trainWordList = []
        self.wordPosiDict = {}
        self.wordVecDict = {}
        self.vocabSize = 0
        self.train_words = 0

    def train(self):
        eda = self.startingEda
        n = 0
        wordCount = 0
        lastWordCount = 0
        wordCountActual = 0
        while n < self.round:
            print "[training] round #" + str(n)
            maxLoss = 0
            for i in range(len(self.trainWordList)):
                if self.trainWordList[i] in self.wordVecDict:
                    if wordCount - lastWordCount > 10000:
                        wordCountActual += (wordCount - lastWordCount)
                        lastWordCount = wordCount
                        # print word_count_actual, self.round * self.train_words + 1, float(word_count_actual) / (self.round * self.train_words + 1)
                        eda = self.startingEda * (1 - float(wordCountActual) / (self.round * self.trainWords + 1))
                        if (eda < self.startingEda * 0.0001):
                            eda = self.startingEda * 0.0001
                        print "[training] No." + str(i) + " word as center", len(self.trainWordList), "in all, eda = ", eda

                    self.train1word(i, eda)
                    word_count += 1
            n += 1

    def train1word(self, index, eda):
        pass

    def calcVecLength(self, vec):
        return np.sqrt(vec.dot(vec))

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

        self.vocabSize = len(self.wordPosiDict)

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
