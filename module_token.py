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




from konlpy.tag import Komoran
from konlpy.tag import Hannanum
import random
from collections import Counter
import json
import glob
# import pytagcloud
import collections
komoran=Komoran()


r=lambda : random.randint(0,255)
color=lambda :(r(),r(),r())

def get_bill_text():
    full_data=""

    #폴더내의 모든 파일 가지고 오기
    files=glob.glob('./app_info/건강/운동/*.json')

    for fname in files:
        print("fname")
        print(fname)

        with open(fname,encoding='UTF8') as json_file:
            json_data=json.load(json_file)
            #key가 app_detail 인 문자열 가지고 오기
            json_string=json_data["app_detail"]
            app_category=json_data["app_category"]
            ### print(json_string)

            #하나의 문자열로 잇는다
            full_data=full_data+json_string+"\n"

    # print(full_data)
    # print(type(full_data))
    # return [line.split("\n")[0] for line in full_data]
    return full_data, app_category

def get_tags(text,ntags=10,multiplier=10):
    h=Hannanum()
    # full_text=""
    # for t in text:
    #     full_text=full_text+" "+t

    nouns=h.nouns(text)
    first_text_nouns=h.nouns(text[0]) #문서군을 계산할때는 필요없음(단일 문서 계산시에만 필요함)

    first_text_count=Counter(first_text_nouns) #문서군을 계산할때는 필요없음(단일 문서 계산시에만 필요함)
    count=Counter(nouns)


    return [{ 'color': color(), 'tag': n, 'size': c*multiplier }\
                for n, c in count.most_common(ntags)],first_text_count,count # ,full_text,first_text_count,count

#word cloud

text, app_category=get_bill_text()
tags, first_text_count, count=get_tags(text)  # tags, full_text, first_text_count, count=get_tags(text)

print(count)



#json 파일로 저장

def file_save(file_name, data, flag):
    if flag=='text':
        a = open(file_name, 'a',encoding="utf-8")
        a.write(data+'\n')

    if flag=='json':
        with open(file_name,'a',encoding="utf-8") as make_file :
            json.dump(data,make_file,ensure_ascii=False,indent='\t')


folder_name='./app_analResult/'+app_category
# file_save(folder_name+'/'+'DF.json',count,'json')#나중에 count를 value를 기준으로 sorting하는 코드 작성(util_sort_jsonfile.py
# file_save(folder_name+'/'+'collect.text',text,'text')#문장으로 저장
# file_save(folder_name+'/'+'collect_nouns.text',komoran.nouns(text),'text')#명사만으로 저장


print(text)
list=komoran.nouns(text)

