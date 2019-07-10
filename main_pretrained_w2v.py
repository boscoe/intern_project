import gensim
import pprint as pt
import json
ko_model = gensim.models.Word2Vec.load('./model/ko/ko.bin') #we vector
#ko_model = gensim.models.fasttext.load_facebook_model("./model/fasttext/ko.bin")


def file_save(file_name, data, flag):
    if flag=='fail':
        a = open(file_name, 'a')
        a.write(data+'\n')

    if flag=='success':
        with open(file_name,'a',encoding="utf-8") as make_file :
            json.dump(data,make_file,ensure_ascii=False,indent='\t')

#words에는 명사만 들어가면 됨(건강/운동 카테고리와 가장 유사한 항목들을 출력)
#dataset은 이전에 있는 데이터들
words = '건강 운동'.split()
# for word in words:
#     print('\n{}'.format(word))
#     pt.pprint(ko_model.wv.most_similar(word))

#json 형식으로 만들고 저장

        # data = {
        #     'app_link': app_link,
        #     'app_category':app_category,
        #     'app_name': app_name,
        #     'app_detail':app_detail
        #
        #     }


app_category="건강/운동"
folder_name='./app_info/'+app_category
for word in words:
    print('\n{}'.format(word))
    pt.pprint(ko_model.wv.most_similar(word))

    data={
        'word':word,
        'sim_list':ko_model.wv.most_similar(word)
    }

    # file_save(folder_name+'/'+'w2v.json', data,'success')
    file_save(folder_name+'/'+'fasttext_vec.json', data,'success')





