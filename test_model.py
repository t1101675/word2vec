from gensim.models import Word2Vec

model = Word2Vec.load("word2vec.model")
word = model.most_similar(positive = ["computer", "system"], negative = ['interface'], topn = 1)
# word = model.similarity('computer', 'human')
print word
