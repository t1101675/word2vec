import numpy as np

f = open("./CBOW6M.model", "r")

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
            #print vecList[0]
            #print vecList[1]
            #print vecList[2]
            # print(aimVec)
            maxCos = -1
            maxWord = ""
            for key, value in wordVecDict.items():
                cosAngle = aimVec.dot(value) / (np.sqrt(aimVec.dot(aimVec)) * np.sqrt(value.dot(value)))
                if cosAngle > maxCos:
                    maxWord = key
                    maxCos = cosAngle

            realCos = aimVec.dot(vecList[3]) / (np.sqrt(aimVec.dot(aimVec)) * np.sqrt(vecList[3].dot(vecList[3])))

            print "target: ", lineList, maxWord, maxCos, realCos

            if maxWord == lineList[3]:
                count += 1

print "all words: ", len(lines), "right: ", count
