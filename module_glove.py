from soynlp.utils import DoublespaceLineCorpus
from soynlp.vectorizer import sent_to_word_contexts_matrix
from glove import Glove
import pprint as pt


#카테고리 데이터로 glove 학습 진행
app_category="건강/운동"
folder_name='./app_analResult/'+app_category
file_name=folder_name+'/'+'collect.txt'

corpus_path = file_name
corpus = DoublespaceLineCorpus(corpus_path, iter_sent=True)

x, idx2vocab = sent_to_word_contexts_matrix(
    corpus,
    windows=3,
    min_tf=10,
    tokenizer=lambda x:x.split(), # (default) lambda x:x.split(),
    dynamic_weight=True,
    verbose=True)

print(x.shape)

glove = Glove(no_components=100, learning_rate=0.05, max_count=30)
glove.fit(x.tocoo(), epochs=5, no_threads=4, verbose=True)

dictionary = {vocab:idx for idx, vocab in enumerate(idx2vocab)}
glove.add_dictionary(dictionary)

words = '건강 운동'.split()
for word in words:
    print('\n{}'.format(word))
    pt.pprint(glove.most_similar(word, number=10))
