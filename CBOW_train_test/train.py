import lib.CBOW as CBOW
import lib.CBOW_neg as CBOW_neg
import os

size = 6

f = open("../data/" + str(size) + "M_train.in", 'r')
# f = open("../data/small.in", 'r')
sentence = f.read()
f.close()

print "OK"
model = CBOW_neg.CBOW(sentence)

# for word in model.wordVecDict:
#     print word + ": ", model.wordVecDict[word]

print "[write] begin write"
f = open("../data/CBOW" + str(size) + "M.model", 'w')
f.write(str(model.vecLength) + "*" + str(model.window) + "*" + str(model.round) + "\n")
for key, value in model.wordVecDict.items():
    f.write(key + "*")
    list = value.tolist()
    for x in list:
        f.write(str(x) + "*")
    f.write("\n")
f.close()
