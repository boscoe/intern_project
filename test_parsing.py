from selenium import webdriver
from bs4 import BeautifulSoup

# setup Driver|Chrome : 크롬드라이버를 사용하는 driver 생성
driver = webdriver.Chrome('C:/Users/USER/chromedriver')
driver.implicitly_wait(3) # 암묵적으로 웹 자원을 (최대) 3초 기다리기

driver.get('https://play.google.com/store/apps') # 구글 플레이 스토어 URL로 이동하기


driver.find_element_by_xpath(
    '//*[@id="fcxH9b"]/div[4]/c-wiz/div/div[2]/div/div[1]/div/c-wiz[1]/c-wiz[3]/div/div[1]/meta'
    ).click() # 버튼클릭하기

driver.find_element_by_xpath(
    '//*[@id="action-dropdown-children-카테고리"]/div/ul/li[1]/ul/li[1]/a'
).click()

driver.find_element_by_xpath(
    '//*[@id="fcxH9b"]/div[4]/c-wiz[2]/div/c-wiz/div/div/c-wiz/c-wiz[1]/c-wiz/div/div[1]/div[1]/a/h2'
).click()



html = driver.page_source # 페이지의 elements모두 가져오기

soup = BeautifulSoup(html, 'html.parser') # BeautifulSoup사용하기





