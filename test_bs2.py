
import requests
from bs4 import BeautifulSoup
import json
import os

## python파일의 위치
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

req = requests.get('https://play.google.com/store/apps')

html = req.text
soup = BeautifulSoup(html, 'html.parser')

num_category = 34
category_name=[]
category_url=[]

str1 = 'div > ul > li:nth-child(1) > ul > li:nth-child('
str2 = ') > a'

for i in range(1,num_category):
    #print(i)
    info = soup.select(
        str1+str(i)+str2
    ) #info는 soup객체들의 list

    #print(info)
    category_url.append(info[0].get('href'))



# print(len(category_url))
# for text in category_url:
#     print(text)



###
req = requests.get(category_url[0])
html = req.text
soup = BeautifulSoup(html, 'html.parser')

list=soup.find_all("div", "W9yFB")

for link in list:
    print(link.get('href'))

