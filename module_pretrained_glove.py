import gensim
from glove import Glove
import pprint as pt
import json
import numpy as np


#########################################################################
app_category="교육" #건강  으로 교체해야됨

# 학습된 glove model load
model = Glove.load('./model/gloves/glove_교육.model') #we vector
fnum=130

words = '별지 행성 별자리 모드 하늘 시계 88 태양 천문 위치 천체 천구 라이브 중심 디스플레이'.split()

#########################################################################

#특정 카테고리와 관련있는 단어를 유사도와 함께 출력함
for w in words:
    # print("운동 , "+w+" = "+str(glove.sim_value("운동",w)))
    print(app_category+" , "+w+" = "+str(model.sim_value(app_category,w)))


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


