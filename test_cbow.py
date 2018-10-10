import CBOW
import build_tree
import os

f = open("../data/word2vec/small_training.txt", 'r')
sentence = f.read()
# print sentence

model = CBOW.CBOW(sentence)
# model.buildWordList()

# print model.trainWordList

for word in model.wordVecDict:
    print word + ": ", model.wordVecDict[word]

# for word in model.wordVecDict:
    # print word + ": ", model.wordPosiDict[word]

# model.buildTree()
# for word in model.tree.wordCodeDict:
    # code = model.tree.wordCodeDict[word]
    # node = model.tree.root
    # for i in range(len(code)):
        # if node is None:
            # raise RuntimeError("code length not right")
        # if code[i] == "0":
            # node = node.left
        # else:
            # node = node.right
    # print word, ", ", code, ", ", node.value
