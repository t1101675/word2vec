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
    text = raw_input("Input 3 words: ")
    lineList = text.split(" ")
    if (lineList < 3):
        print "At least 3 words"
        continue

    vecList = []
    for word in lineList:
        if word in wordVecDict:
            vecList.append(wordVecDict[word])
        else:
            print word, " not in dict"
            break
    if len(vecList) < 3:
        continue;

    aimVec = vecList[1] - vecList[0] + vecList[2]
    aimLen = np.sqrt(aimVec.dot(aimVec))
    aimVec /= aimLen
    maxWords = [("", -1) for i in range(maxNum)]
    for key, value in wordVecDict.items():
        if key == lineList[0]:
            continue
        if key == lineList[1]:
            continue
        if key == lineList[2]:
            continue
        cosAngle = aimVec.dot(value)
        for i in range(len(maxWords)):
            if cosAngle > maxWords[i][1]:
                maxWords.insert(i, (key, cosAngle))
                maxWords.pop()
                break

    for pair in maxWords:
        print pair
