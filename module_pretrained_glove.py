import gensim
from glove import Glove
import pprint as pt
import json
import numpy as np


#########################################################################
app_category="스포츠" #건강  으로 교체해야됨

# 학습된 glove model load
model = Glove.load('./model/gloves/glove.model') #we vector
fnum=337

words = '목록 축구관련 백만건 유료버전 푸시경고 최신스코어 시합통계 교체선수 리그뉴스 클럽뉴스 최고득점자 선호팀 축구리그들'.split()

#########################################################################

#특정 카테고리와 관련있는 단어를 유사도와 함께 출력함
for w in words:
    print(app_category+" , "+w+" = "+str(model.sim_value(app_category,w)))


##########################################################################


# 가중치 최종 계산

fname="./app_TFIDF/"+app_category+"/"+str(fnum)+"_TFIDF.json"

with open(fname,encoding='UTF8') as json_file:
    json_data=json.load(json_file)

    for w in words:
        tf_idf_weight=json_data[w]
        tf_idf_weight=float(tf_idf_weight)

        sim_weight=model.sim_value(app_category,w)

        weight=tf_idf_weight*sim_weight

        print(w+", "+str(weight))


#####################################################3
#### 키워들 간의 유사도#####
###############################################


for w in words:
    for j in words:
        if w!=j:
            # print(w+" , "+j+" = "+str(model.sim_value(w,j)))

            tf_idf_weight_w=json_data[w]
            tf_idf_weight_w=float(tf_idf_weight_w)

            tf_idf_weight_j=json_data[w]
            tf_idf_weight_j=float(tf_idf_weight_j)

            sim_weight=model.sim_value(w,j)

            weight=(tf_idf_weight_w+tf_idf_weight_j)/2+sim_weight

            print(w+", "+str(weight))

