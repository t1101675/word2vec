import lib.CBOW as CBOW
import os

f = open("../data/4M_train.in", 'r')
sentence = f.read()
f.close()

model = CBOW.CBOW(sentence)

# for word in model.wordVecDict:
#     print word + ": ", model.wordVecDict[word]

f = open("./CBOW.model", 'w')
f.write(str(model.vecLength) + " " + str(model.window) + " " + str(model.round) + "\n")
for key, value in model.wordVecDict.items():
    f.write(key + " ")
    list = value.tolist()
    for x in list:
        f.write(str(x) + " ")
    f.write("\n")
