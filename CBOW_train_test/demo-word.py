import numpy as np

size = 100
maxNum = 10

f = open("../data/CBOW" + str(size) + "M.model", "r")

lines = f.readlines()
#get info
info = lines[0].split("*")
vecLength = int(info[0])
window = int(info[1])
round = int(info[2])

#get word2vec
wordVecDict = {}
i = 0
for i in range(1, len(lines)):
    L = lines[i].split("*")
    vecList = [float(x) for x in L[1: vecLength + 1]]
    wordVecDict[L[0]] = np.array(vecList)

# normalize
for key in wordVecDict:
    length = np.sqrt(wordVecDict[key].dot(wordVecDict[key]))
    wordVecDict[key] /= length

while True:
    word = raw_input("Input a word: ")
    if word not in wordVecDict:
        print word, " not in dict"
        continue
    aimVec = wordVecDict[word]
    pairList = [(word, value.dot(aimVec)) for word, value in wordVecDict.items()]
    sortedPairList = sorted(pairList, key=lambda pair:pair[1], reverse = True)
    resultList = sortedPairList[1: maxNum + 1] #ignore the word itself
    for pair in resultList:
        print pair
