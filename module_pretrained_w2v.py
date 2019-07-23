import gensim
import pprint as pt
import json
ko_model = gensim.models.Word2Vec.load('./model/ko/ko.bin') #we vector

def file_save(file_name, data, flag):
    if flag=='fail':
        a = open(file_name, 'a')
        a.write(data+'\n')

    if flag=='success':
        with open(file_name,'a',encoding="utf-8") as make_file :
            json.dump(data,make_file,ensure_ascii=False,indent='\t')


############################ main.py
words = '목록 축구 관련 백만 건 유료 버전 푸시 경고 최신 스코어 시합 통계 교체 선수 리그 뉴스 클럽 뉴스 최고 득점자 선호 팀 축구 리그 들'.split() #이곳은 각 애플리케이션 문서의 키워드가 들어있음(키워드는 tf-
fnum=337
app_category="스포츠"
folder_name='./app_info/'+app_category

# for word in words:
#     print('\n{}'.format(word))
#     pt.pprint(ko_model.wv.similarity(app_category,word))


#################################### final weight
fname="./app_TFIDF/"+app_category+"/"+str(fnum)+"_TFIDF.json"

with open(fname,encoding='UTF8') as json_file:
    json_data=json.load(json_file)

    for w in words:
        tf_idf_weight=json_data[w]
        tf_idf_weight=float(tf_idf_weight)

        sim_weight=ko_model.wv.similarity(app_category,w)
        sim_weight=float(sim_weight)

        weight=tf_idf_weight*sim_weight

        print(w+", "+str(weight))





