from sklearn.feature_extraction.text import TfidfVectorizer
from collections import defaultdict
import json
import glob
import os
from konlpy.tag import Hannanum


# 하나의 문서군에 대해서 실행할 수 있음
# 자동화하기 위해서 모든 카테고리에 대해 동일하게 실행하면 되는듯
# 단어의 DF값은 이미 다른 파일에서 저장하므로 ㄱㅊ


#########저장하는 문서##########  => TR-IDF 문서를 저장함
#TF-IDF.json 파일을 저장함


cate="교육"
file_dir='./app_info/'+cate #여기만 바뀌면 됨



idx_list=list()#TFIDF.json파일의 인덱스를 맞춰 넣기 위해서 미리 저장해두고 나중에 save시에 빼서 사용함

def get_text():
    full_data=""

    #폴더내의 모든 파일 가지고 오기
    files=glob.glob(file_dir+'/*.json')
    corpus=list()
    h = Hannanum()

    for fname in files:
        # print("fname")
        print(fname)
        file_name=fname.split('\\')[1]
        file_idx=file_name.split('.')[0]
        print(file_idx) #이게 파일이름이지뭐...
        idx_list.append(file_idx) #*json파일을 읽었는데, 읽은 순서를 저장하고 싶으면 이렇게 하면됨

        with open(fname,encoding='UTF8') as json_file:
            json_data=json.load(json_file)
            #key가 app_detail 인 문자열 가지고 오기

            json_string=json_data["app_detail"]# 개별문자
            # corpus.append(json_string)#=>이걸 사용해서 corpus를 만들면 명사만 엮인게 아니라서 이상한 애들이 많이 들어감

            #corpus에 명사만 담기 위함(형태소 자르기)

            nouns=h.nouns(json_string)

            #list를 string으로 변환
            nouns=' '.join(nouns) #list의 element들을 공백을 이용해서 구분함

            # print("nouns 출력")
            # print(nouns)
            corpus.append(nouns) #corpus에 명사만 담을 것임!
            ######

            app_category=json_data["app_category"]
            ### print(json_string)

    return full_data, app_category,corpus


def file_save(file_name, data, flag,folder_name):
    # 디렉토리가 없으면 일단 생성
    if not os.path.isdir(folder_name):
            #파일이 없으면 생성함
            os.mkdir(folder_name)
            print("만들어라")
    else:
        print("있다..?")

    if flag=='text':
        a = open(file_name, 'a',encoding="utf-8")
        a.write(data+' ')

    if flag=='json':
        with open(file_name,'a',encoding="utf-8") as make_file :
            json.dump(data,make_file,ensure_ascii=False,indent='\t')

#
# corpus = ['동해물과 백두산이 마르고 닳도록 하느님이 보우하사 우리나라 만세 무궁화 삼천리 화려 강산 대한사람 대한으로 길이 보전하세',
#           '남산 위에 저 소나무 철갑을 두른 듯 바람서리 불변함은 우리 기상일세 무궁화 삼천리 화려 강산 대한사람 대한으로 길이 보전하세',
#           '가을 하늘 공활한데 높고 구름 없이 밝은 달은 우리 가슴 일편단심일세 무궁화 삼천리 화려 강산 대한사람 대한으로 길이 보전하세',
#           '이 기상과 이 맘으로 충성을 다하여 괴로우나 즐거우나 나라 사랑하세 무궁화 삼천리 화려 강산 대한사람 대한으로 길이 보전하세',
#           '오 필승 코리아 오 필승 코리아 오 필승 코리아 오 오레 오레 무궁화 삼천리 화려 강산 대한사람 대한으로 길이 보전하세']
#

full_data,app_category,corpus=get_text()

if '/' in app_category: # / 기호가 있으면 잘라서 앞에만 가져오기
    app_category=app_category.split('/')[0]
# ============================================
# -- Get TFIDF
# ============================================
vectorizer = TfidfVectorizer()
sp_matrix = vectorizer.fit_transform(corpus)

word2id = defaultdict(lambda : 0)

for idx, feature in enumerate(vectorizer.get_feature_names()):
    word2id[feature] = idx

# tfidf_list=list()
for i, sent in enumerate(corpus):  # word2id[token] 특정 단어의 id값을 반환
    print('====== document[%d] ======' % i)

    # print( [ (token, sp_matrix[i, word2id[token]]) for token in sent.split() ] )
    tfidf_list=dict()
    tfidf_dict=dict()

    folder_name='./app_TFIDF/'+app_category
    for token in sent.split():
        tfidf_list[token]=sp_matrix[i, word2id[token]]

    #정렬후 출력
    tfidf_list=sorted(tfidf_list.items(), key=(lambda element: element[1]),reverse=True)

    for element in tfidf_list:
        tfidf_dict[element[0]]=str(element[1])

    # print(tfidf_dict)

    #json file로 저장
    file_save(folder_name+'/'+idx_list[i]+'_TFIDF.json',tfidf_dict,'json',folder_name)

print(corpus[0])



