from soynlp.utils import DoublespaceLineCorpus
from soynlp.vectorizer import sent_to_word_contexts_matrix
from glove import Glove

import pprint as pt



#카테고리 데이터로 glove 학습 진행
app_category="스포츠" #건강  으로 교체해야됨
folder_name='./app_analResult/'+app_category
file_name=folder_name+'/'+'collect_nouns.txt' #명사만 있는 텍스트 파일


corpus_path = file_name
corpus = DoublespaceLineCorpus(corpus_path, iter_sent=True)

x, idx2vocab = sent_to_word_contexts_matrix(
    corpus,
    windows=3, #고려할 앞뒤 단어의 개수
    min_tf=10, #10회 이하의 단어 무시
    tokenizer=lambda x:x.split(), # (default) lambda x:x.split(),
    dynamic_weight=True,
    verbose=True)

print(x.shape)

glove = Glove(no_components=100, learning_rate=0.05, max_count=30)
model=glove.fit(x.tocoo(), epochs=10, no_threads=4, verbose=True)

# 모델 저장
# glove.save('glove.model')

dictionary = {vocab:idx for idx, vocab in enumerate(idx2vocab)}
glove.add_dictionary(dictionary)

# 	"연속": "0.3980962747909026",
# 	"만보계": "0.28908399301053456",
# 	"카운팅": "0.2843544819935018",
# 	"시작": "0.21446109488441178",
# 	"중지": "0.20888132162673734",
# 	"그래프": "0.1654301671420144",

words = '연속 만보계 카운팅 시작 중지 그래프'.split() #이곳은 각 애플리케이션 문서의 키워드가 들어있음(키워드는 tf-idf로 추출함)
# for word in words:
#     print('\n{}'.format(word))
#     pt.pprint(glove.most_similar(word, number=10))


# print(glove.most_similar('운동', numbehttps://play.google.com/store/apps/category/FAMILY_PRETEND/collection/topselling_freer=6))
# print(glove.sim_value('운동','제공')) #0
# print(glove.sim_value('집')) #24


#특정 카테고리와 관련있는 단어를 유사도와 함께 출력함
for w in words:
    # print("운동 , "+w+" = "+str(glove.sim_value("운동",w)))
    print(app_category+" , "+w+" = "+str(glove.sim_value(app_category,w)))



