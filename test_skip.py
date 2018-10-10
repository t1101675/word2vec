import skip_gram
import build_tree
import os
f = open("../data/word2vec/small_training.txt", 'r')
# f = open("1M_test.in", "r")
sentence = f.read()

model = skip_gram.SkipGram(sentence)

for word in model.wordVecDict:
    print word + ": ", model.wordVecDict[word]
