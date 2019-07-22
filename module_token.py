# from konlpy.tag import Komoran
# komoran = Komoran()
# print(komoran.morphs(u'우왕 코모란도 오픈소스가 되었어요'))
# print(komoran.nouns(u'오픈소스에 관심 많은 멋진 개발자님들!'))
# print(komoran.pos(u'한글형태소분석기 코모란 테스트 중 입니다.'))
#
# #결과
# ['우왕', '코', '모란', '도', '오픈소스', '가', '되', '었', '어요']
# ['오픈소스', '관심', '개발자']
# [('한글', 'NNG'), ('형태소', 'NNP'), ('분석기', 'NNG'), ('코모', 'NNP'), ('란', 'JX'), ('테스트', 'NNG'), ('중', 'NNB'), ('이', 'VCP'), ('ㅂ니다', 'EF'), ('.', 'SF')]


#  각기 다른 파일을 만들어주는 module_token.py
# DF.json   =>카테고리 해당 문서군
# collect.txt =>카테고리 해당 문서군
# collect_nouns.txt =>카테고리 해당 문서군(의 명사만 모았음)
# 각 애플리케이션 문서당 1_TF.json
# 각 애플리케이션 문서당 1_nouns.json


from konlpy.tag import Komoran
from konlpy.tag import Hannanum
import random
from collections import Counter
import json
import glob
# import pytagcloud
import collections
komoran=Komoran()
h = Hannanum()

r=lambda : random.randint(0,255)
color=lambda :(r(),r(),r())

def get_bill_text():
    full_data=""

    #여기만 바꾸면됨!
    change_cate='스포츠'
    file_dir='./app_info/'+change_cate+'/*.json'

    #폴더내의 모든 파일 가지고 오기
    files=glob.glob(file_dir)

    for fname in files:
        print("fname")
        print(fname)
        file_name=fname.split('\\')[1]
        file_idx=file_name.split('.')[0]
        print(file_idx)

        with open(fname,encoding='UTF8') as json_file:
            json_data=json.load(json_file)
            #key가 app_detail 인 문자열 가지고 오기

            json_string=json_data["app_detail"]
            app_category=json_data["app_category"]
            ### print(json_string)

            # 문서 개별 TR값을 계산하기 위함
            cal_tf(json_string,file_idx,app_category)

            #하나의 문자열로 잇는다
            full_data=full_data+json_string+"\n"

    # print(full_data)
    # print(type(full_data))
    # return [line.split("\n")[0] for line in full_data]
    return full_data, app_category


def cal_tf(document_contents,file_idx,app_category):

    if '/' in app_category: # / 기호가 있으면 잘라서 앞에만 가져오기
        app_category=app_category.split('/')[0]


    #애플리케이션 한개의 문서의 Term Frequency만 저장
    folder_name='./app_TF/'+app_category

    tags, first_text_count, count=get_tags(document_contents)
    file_save(folder_name+'/'+file_idx+'_TF.json',count,'json')  #여기! 주석해제


    nouns=h.nouns(document_contents)


##############################명사 저장할거야
    #애플리케이션 한개의 문서의 명사만 저장
    folder_name='./app_nouns/'+app_category

# 여기! 주석해제
#     sdata=""
#     for n in nouns:
#         sdata=sdata+" "+n
#     file_save(folder_name+'/'+file_idx+'_nouns.txt',sdata,'text')#명사만으로 저장


def get_tags(text,ntags=10,multiplier=10):
    # h=Hannanum()
    # full_text=""
    # for t in text:
    #     full_text=full_text+" "+t

    nouns=h.nouns(text)
    first_text_nouns=h.nouns(text[0]) #문서군을 계산할때는 필요없음(단일 문서 계산시에만 필요함)

    first_text_count=Counter(first_text_nouns) #문서군을 계산할때는 필요없음(단일 문서 계산시에만 필요함)
    count=Counter(nouns)


    return [{ 'color': color(), 'tag': n, 'size': c*multiplier }\
                for n, c in count.most_common(ntags)],first_text_count,count # ,full_text,first_text_count,count



#json 파일로 저장

def file_save(file_name, data, flag):
    if flag=='text':
        a = open(file_name, 'a',encoding="utf-8")
        a.write(data+' ')

    if flag=='json':
        with open(file_name,'a',encoding="utf-8") as make_file :
            json.dump(data,make_file,ensure_ascii=False,indent='\t')



##################################################################
#word cloud

text, app_category=get_bill_text()

if '/' in app_category: # / 기호가 있으면 잘라서 앞에만 가져오기
    app_category=app_category.split('/')[0]

# folder_name='./app_analResult/'+app_category
folder_name='./app_analResult/'+app_category

tags, first_text_count, count=get_tags(text)  # tags, full_text, first_text_count, count=get_tags(text)

print(count)


file_save(folder_name+'/'+'DF.json',count,'json')#나중에 count를 value를 기준으로 sorting하는 코드 작성(util_sort_jsonfile.py
file_save(folder_name+'/'+'collect.txt',text,'text')#문장으로 저장

h = Hannanum()
nouns=h.nouns(text)
print(len(nouns))


#여기서 전체 문장에서 명사를 뽑아와야된다.
data=""
for n in nouns:
    data=data+" "+n

file_save(folder_name+'/'+'collect_nouns.txt',data,'text')#명사만으로 저장



