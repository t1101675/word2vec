from gensim.test.utils import common_texts, get_tmpfile
from gensim.models import word2vec
from gensim.models import KeyedVectors


path = get_tmpfile("word2vec.model")

sentences = word2vec.LineSentence('./data/word2vec/small_training.txt')

print "OK"

model = word2vec.Word2Vec(sentences, size = 100, window = 5, min_count = 1, workers = 4)

print "OK2"
model.save("word2vec.model")

print model.most_similar(positive=['spanish', 'society'], negative=['work'], topn=1)
print word2vec.__file__
