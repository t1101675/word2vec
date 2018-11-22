import numpy as np

size = 10
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

for key in wordVecDict:
    len = np.sqrt(wordVecDict[key].dot(wordVecDict[key]))
    wordVecDict[key] /= len
    print wordVecDict[key]


f2 = open("../data/analogy.in")

lines = f2.readlines()
count = 0

# print wordVecDict['translations']

for line in lines:
    if line[0] == ":":
        continue
    else:
        lineList = line.split()
        vecList = []
        # print lineList
        for word in lineList:
            if word not in wordVecDict:
                break;
            else:
                # print word, "in"
                vecList.append(wordVecDict[word])
                # print word, wordVecDict[word]
        else:
            #all in wordlist
            print "all word in word vec"
            aimVec = vecList[1] - vecList[0] + vecList[2]
            aimLen = np.sqrt(aimVec.dot(aimVec))
            aimVec /= aimLen
            maxCos = -1
            maxWords = [("", -1) for i in range(maxNum)]
            for key, value in wordVecDict.items():
                if key == lineList[0]:
                    continue
                if key == lineList[1]:
                    continue
                if key == lineList[2]:
                    continue
                cosAngle = aimVec.dot(value)
                if cosAngle > maxCos:
                    maxWord = key
                    maxCos = cosAngle

            realCos = aimVec.dot(vecList[3])

            print "target: ", lineList, maxWord, maxCos, realCos

            if maxWord == lineList[3]:
                count += 1

print "all words: ", len(lines), "right: ", count
