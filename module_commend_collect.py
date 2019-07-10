import requests as rq
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin, parse_qs
from selenium import webdriver
import json
import os
from collections import OrderedDict
file_data=OrderedDict()

TOP_URL = "https://play.google.com/store"
BASE_URL = "https://play.google.com"


import re

class ops :
    save_app_count=1

    def inc(self):
        self.save_app_count=self.save_app_count+1

utils=ops()

def make_payload(page):
    return "start=%s&num=60&numChildren=0&cctcss=tall-cover&cllayout=NORMAL"%(page)


def connect_category(url):

    querystring = {"authuser": "0"}

    start = 0
    targets = list()
    pre_count = len(targets)
    current_count = len(targets)

    is_last = False

    while not is_last:
        payload = make_payload(start)
        headers = {
            'content-type': "text/html; charset=utf-8",
            'cache-control': "no-cache",
            'user-agen': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
        }

        res = rq.post(url, data=payload, headers=headers, params=querystring)
        cate_soup = BeautifulSoup(res.content, 'html.parser')
        pre_count = len(targets)
        current_soup = cate_soup.select('.card-content .details a.title')


        for s in current_soup:
            is_exist = False

            data = {'title': s.get('title'), 'link': urljoin(BASE_URL, s.get('href')), 'queryString': parse_qs(urlparse(s.get('href')).query)['id'][0]}

            for target in targets:
                if data['queryString'] == target['queryString']:
                    is_exist = True
            if not is_exist:
                targets.append(data)


        current_count = len(targets)

        if current_count == pre_count:
            is_last = True

        start += 60

    return targets



def get_category():
    # lines = open('googleplay_catepory_link.txt', 'r').readlines()
    lines = open('1.txt', 'r').readlines()

    return [line.split('\n')[0] for line in lines]



def file_save(file_name, data, flag):
    if flag=='fail':
        a = open(file_name, 'a')
        a.write(data+'\n')

    if flag=='success':
        with open(file_name,'a',encoding="utf-8") as make_file :
            json.dump(data,make_file,ensure_ascii=False,indent='\t')


driver=webdriver.Chrome('chromedriver') #현재 경로에 있는 chromdriver.exe 를 넣는다




def data_parse(link):
    try:
        # print(link)

        driver.get(link)
        html=driver.page_source
        # soup = BeautifulSoup(html, 'html.parser',from_encoding='utf-8')
        soup = BeautifulSoup(html, 'html.parser')

        app_link=link #application url
        app_detail_list=soup.findAll('div', class_='W4P4ne') #application 설명
        app_name_list=soup.findAll('h1',class_='AHFaub')
        app_category_list=soup.findAll('span',class_='T32cc UAO9ie')

        #정보 정제
        app_detail=app_detail_list[0].meta["content"]
        app_name=app_name_list[0].span.text

        # print(len(app_category_list))
        for element in app_category_list:
            match_str=element.a.get("itemprop")

            if match_str == 'genre':
                app_category=element.a.text


        print("=========app 설명 시작===========")
        print(app_link)
        print(app_category)
        print(app_name)
        print(app_detail)
        print("=========app 설명 끝=============")

        data = {
            'app_link': app_link,
            'app_category':app_category,
            'app_name': app_name,
            'app_detail':app_detail

            }

        # 폴더가 없으면 생성함
        folder_name='./app_info/'+app_category
        print(folder_name)
        if not os.path.isdir(folder_name):
            #파일이 없으면 생성함
            os.mkdir(folder_name)
            print("만들어라")
        else:
            print("있다..?")

        file_save(folder_name+'/'+str(utils.save_app_count)+'.json', data,'success')
        utils.inc()

    except:
        file_save('error.txt', link,'fail')


if __name__ ==  "__main__":
    print('commend collecting crawler')

    categories = get_category()
    for category_link in categories:
        targets = connect_category(category_link)

        print("애플리케이션 개수")
        print(len(targets))

        for target in targets:
            data_parse(target['link'])
