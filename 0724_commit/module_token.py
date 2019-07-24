import time
## 0724 수정
from konlpy.tag import Hannanum
#####
from konlpy.tag import Okt
import os
from collections import Counter
import json
import glob

## 0724 수정
# h = Hannanum()
h=Okt()
#####

s=time.time()

def get_bill_text():
    full_data=""
    nouns_list=""

    #여기만 바꾸면됨!
    change_cate='스포츠'
    file_dir='./app_info/'+change_cate+'/*.json'

    #폴더내의 모든 파일 가지고 오기
    files=glob.glob(file_dir)

    for fname in files:
        file_name=fname.split('\\')[1]
        file_idx=file_name.split('.')[0]
        print(file_idx)

        with open(fname,encoding='UTF8') as json_file:
            json_data=json.load(json_file)
            #key가 app_detail 인 문자열 가지고 오기

            json_string=json_data["app_detail"]
            app_category=json_data["app_category"]


            # 문서 개별 TR값을 계산하기 위함
            reValue=cal_tf(json_string,file_idx,app_category)
            nouns_list=nouns_list+" "+reValue

            #하나의 문자열로 잇는다
            full_data=full_data+"\n"+json_string

    return full_data, app_category,nouns_list


def cal_tf(document_contents,file_idx,app_category):

    if '/' in app_category: # / 기호가 있으면 잘라서 앞에만 가져오기
        app_category=app_category.split('/')[0]


    #애플리케이션 한개의 문서의 Term Frequency만 저장
    folder_name='./app_TF/'+app_category
    count, nouns=get_tags(document_contents)
    file_save(folder_name+'/'+file_idx+'_TF.json',count,'json',folder_name)  #여기! 주석해제


    folder_name='./app_nouns/'+app_category

    # 여기! 주석해제
    noun_list=""
    for n in nouns:
        noun_list=noun_list+" "+n
    file_save(folder_name+'/'+file_idx+'_nouns.txt',noun_list,'text',folder_name)#명사만으로 저장

    return noun_list #문서 하나 / 명사들만 붙여둔 string을 반환

def get_tags(text,ntags=10,multiplier=10):

    nouns=h.nouns(text)
    # first_text_nouns=h.nouns(text[0]) #문서군을 계산할때는 필요없음(단일 문서 계산시에만 필요함)
    #
    # first_text_count=Counter(first_text_nouns) #문서군을 계산할때는 필요없음(단일 문서 계산시에만 필요함)
    count=Counter(nouns)

    return count,nouns # ,full_text,first_text_count,count


#json 파일로 저장
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


text, app_category,nouns_list=get_bill_text()

if '/' in app_category: # / 기호가 있으면 잘라서 앞에만 가져오기
    app_category=app_category.split('/')[0]

# folder_name='./app_analResult/'+app_category
folder_name='./app_analResult/'+app_category



# print(count)


file_save(folder_name+'/'+'collect.txt',text,'text',folder_name)#문장으로 저장
file_save(folder_name+'/'+'collect_nouns.txt',nouns_list,'text',folder_name)#명사만으로 저장


################################DF.json 지금 필요없어서 일단 보류.. 시간 여기서 많이 걸림##############
# count, nouns=get_tags(text)  # tags, full_text, first_text_count, count=get_tags(text)
# file_save(folder_name+'/'+'DF.json',count,'json',folder_name)#나중에 count를 value를 기준으로 sorting하는 코드 작성(util_sort_jsonfile.py
##################################################################################################

e=time.time()
print(e-s)
