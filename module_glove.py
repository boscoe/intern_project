from soynlp.utils import DoublespaceLineCorpus
from soynlp.vectorizer import sent_to_word_contexts_matrix
from glove import Glove
import json
import pprint as pt



#카테고리 데이터로 glove 학습 진행
app_category="교육" #건강  으로 교체해야됨
fnum=130
#################################################

# folder_name='./app_analResult/'+app_category
# file_name=folder_name+'/'+'collect_nouns.txt' #명사만 있는 텍스트 파일

##################################################################
file_name='./dataset/collect_nouns.txt'

corpus_path = file_name
corpus = DoublespaceLineCorpus(corpus_path, iter_sent=True)

x, idx2vocab = sent_to_word_contexts_matrix(
    corpus,
    windows=10, #고려할 앞뒤 단어의 개수
    min_tf=0, #10회 이하의 단어 무시
    tokenizer=lambda x:x.split(), # (default) lambda x:x.split(),
    dynamic_weight=True,
    verbose=True)

print(x.shape)

glove = Glove(no_components=100, learning_rate=0.05, max_count=30)
glove.fit(x.tocoo(), epochs=10, no_threads=4, verbose=True)

dictionary = {vocab:idx for idx, vocab in enumerate(idx2vocab)}
glove.add_dictionary(dictionary)

# 모델 저장
# glove.save('./model/gloves/glove_교육.model')

########################################
words = '별지 행성 별자리 모드 하늘 시계 88 태양 천문 위치 천체 천구 라이브 중심 디스플레이'.split() #이곳은 각 애플리케이션 문서의 키워드가 들어있음(키워드는 tf-idf로 추출함)



#특정 카테고리와 관련있는 단어를 유사도와 함께 출력함
for w in words:
    # print("운동 , "+w+" = "+str(glove.sim_value("운동",w)))
    print(app_category+" , "+w+" = "+str(glove.sim_value(app_category,w)))


# 가중치 최종 계산

fname="./app_TFIDF/"+app_category+"/"+str(fnum)+"_TFIDF.json"

with open(fname,encoding='UTF8') as json_file:
    json_data=json.load(json_file)

    for w in words:
        tf_idf_weight=json_data[w]
        tf_idf_weight=float(tf_idf_weight)

        sim_weight=glove.sim_value(app_category,w)

        weight=tf_idf_weight*sim_weight

        print(w+", "+str(weight))

