import lib.CBOW as CBOW
import os

size = 6

f = open("../data/" + str(size) + "M_train.in", 'r')
sentence = f.read()
f.close()

model = CBOW.CBOW(sentence)

# for word in model.wordVecDict:
#     print word + ": ", model.wordVecDict[word]

print "[write] begin write"
f = open("./CBOW" + str(size) + "M.model", 'w')
f.write(str(model.vecLength) + "*" + str(model.window) + "*" + str(model.round) + "\n")
for key, value in model.wordVecDict.items():
    if 'alphabet' in key:
        print len(key), key, ": ", value
    if len(value) < model.vecLength:
        print key
    f.write(key + "*")
    list = value.tolist()
    for x in list:
        f.write(str(x) + "*")
    f.write("\n")
f.close()
