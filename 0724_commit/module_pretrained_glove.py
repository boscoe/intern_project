import gensim
from glove import Glove
import pprint as pt
import json
import numpy as np


#########################################################################
app_category="스포츠" #건강  으로 교체해야됨

# 학습된 glove model load
model = Glove.load('./model/gloves/glove_스포츠_twitter.model') #we vector
# model = Glove.load('./model/gloves/glove_교육.model') #we vector

fnum=337

######## words 생성
words=""

fname="./app_TFIDF/"+app_category+"/"+str(fnum)+"_TFIDF.json"
# fname="./app_TFIDF/"+app_category+"_hannanum/"+str(fnum)+"_TFIDF.json"

with open(fname,encoding='UTF8') as json_file:
    json_data=json.load(json_file)

    for key in json_data.keys():
        words=words+key+" "

    # print(words)

words=words.split()

########################################################################
#### 키워드 먼저 추출하는 경우####

w_count=0
w_list=""
w_th=15 # top n개의 키워드를 우선 추출

for w in words:
    if w_count < w_th:
        w_list=w_list+w+" "
        w_count+=1

words=w_list
words=words.split()

print(words)
#########################################################################
# 분석
result=dict()
########################################################################
# keyword vs category sim 값
for w in words:
    # print(app_category+" , "+w+" = "+str(model.sim_value(app_category,w)))
    result[app_category+","+w]=model.sim_value(app_category,w)

print("category vs keyword sim")
print(sorted(result.items(), key=lambda t : abs(t[1])))
print("===================================================")
##########################################################################
# key word vs category 끼리의 최종 weight
result=dict() #초기화

for w in words:
    tf_idf_weight=json_data[w]
    tf_idf_weight=float(tf_idf_weight)

    sim_weight=model.sim_value(app_category,w)

    weight=tf_idf_weight+abs(sim_weight)
    # weight=tf_idf_weight*sim_weight

    # print(w+", "+str(weight))
    result[app_category+","+w]=weight

print("category vs keyword final weight")
print(sorted(result.items(), key=lambda t : abs(t[1])))
print("===================================================")
####################################################
#### 키워들 간의 유사도#####
###############################################
result=dict() #초기화
weight_threshold=0.7
final_result=dict()

for w in words:
    for j in words:
        if w!=j:
            # print(w+" , "+j+" = "+str(model.sim_value(w,j)))

            tf_idf_weight_w=json_data[w]
            tf_idf_weight_w=float(tf_idf_weight_w)

            tf_idf_weight_j=json_data[w]
            tf_idf_weight_j=float(tf_idf_weight_j)

            sim_weight=model.sim_value(w,j)

            weight=((tf_idf_weight_w+tf_idf_weight_j))+abs(sim_weight)
            # weight=(tf_idf_weight_w+tf_idf_weight_j)/2+sim_weight

            # print(w+", "+str(weight))

            if weight >=weight_threshold:
                result[w+","+j]=weight

                # freq counting
                if w in final_result.keys():
                    final_result[w]+=1
                else :
                    final_result[w]=1

                if j in final_result.keys():
                    final_result[j]+=1
                else :
                    final_result[j]=1


print("keyword vs keyword final")
print(sorted(result.items(), key=lambda t : abs(t[1])))
print("===================================================")

sum=0
for key in final_result.keys():
    val=final_result[key]
    sum+=abs(val)

########################
## 정규화
for key in final_result.keys():
    final_result[key]=final_result[key]/sum

########################
print("keyword vs keyword finals freq")
print(sorted(final_result.items(), key=lambda t : abs(t[1])))

