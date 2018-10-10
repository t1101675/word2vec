class CBOW:
    def __init__(self, sentence, minCount = 1, vecLength = 20, window = 5):
        self.sentence = sentence
        self.minCount = minCount
        self.vecLength = vecLength
        self.window = window
        self.eda = 0.05
        self.neg =
        self.trainWordList = []
        self.wordPosiDict = {}
        self.wordVecDict = {}
    def train(self):
        buildWordList()


    def sig(self, x):
        # print "x: ", x
        return 1 / (1 + np.exp(-x))

    def buildWordList(self):
        self.trainWordList = self.sentence.split(" ")
        for word in self.trainWordList:
            if word in self.wordPosiDict:
                self.wordPosiDict[word] += 1
            else:
                self.wordPosiDict[word] = 1
                self.wordVecDict[word] = np.random.rand(1, self.vecLength)
