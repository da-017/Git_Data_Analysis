# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from selenium import webdriver 
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from bs4 import BeautifulSoup 
import time
import datetime
from pytz import timezone

import pandas as pd

import warnings
warnings.filterwarnings('ignore')

#웹드라이버 설정
options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox') # 보안 기능인 샌드박스 비활성화
options.add_argument('--disable-dev-shm-usage') # dev/shm 디렉토리 사용 안함
service = ChromeService(executable_path=ChromeDriverManager().install()) #새로운 버전 
driver = webdriver.Chrome(service=service, options=options)  #웹오픈
#웹 드라이버의 버전과 크롬의 버전이 같아야 한다.

driver.set_window_size(800, 800)

driver.get('https://youtu.be/-yz5_l61QHk?si=o3zCAWxX637IPurW')
driver.get('https://www.youtube.com/watch?v=RHZb_u3VOco')

#크롤링========================
driver.implicitly_wait(10) #로딩하는 시간 10s,로딩되면 바로 끝 >>최대 10초 기다린다

#사람인척하기 차단을 안 당하려면
driver.execute_script('window.scrollTo(0,800)') #0부터 화면창끝까지 내리기
time.sleep(5)

#댓글 수집을 위한 스크롤 내리기  
last_height = driver.execute_script('return document.documentElement.scrollHeight')
#마지막 세로 길이를 리턴
print(last_height)
while True:
    print('스크롤 중...')
    driver.execute_script('window.scrollTo(0, document.documentElement.scrollHeight)') #스크롤을 내림
    time.sleep(5)  #로딩대기 시간이 있어서 길게 늘려줘야 조기종료 막음
    new_height= driver.execute_script('return document.documentElement.scrollHeight')
    
    #현재 스크롤과 과거 스클로 사이즈 비교
    if new_height==last_height:  #스크롤이 없음
        break
    
    #혅재 last 변수에 담음
    last_height=new_height
    time.sleep(5)
    
print('스크롤 종료')
print('댓글 수집 시작')



#댓글 수집
html_source=driver.page_source
soup=BeautifulSoup(html_source,'html.parser')

#댓글 리스트 가져오기
comment_list =soup.select('yt-attributed-string#content-text') #id로 가져오기
comment_final=[]

print('댓글수:',str(len(comment_list)))


#댓글 텍스트 추출
for i in range(len(comment_list)):
    temp_comment=comment_list[i].text
    #전처리  
    temp_comment=temp_comment.replace('\n',' ').strip() #엔터를 없애고 연결 / 앞뒤공백이 있다면 삭제
    print(temp_comment)
    comment_final.append(temp_comment)  #댓글내용 리스트에 담기
    
#DF 만들고 저장(list > dic > df)
youtube_dic={'댓글내용':comment_final}
youtube_df=pd.DataFrame(youtube_dic)
print('='*50)
print('크롤링 종료')
print('='*50)

#정상 수집 확인
print(youtube_df.info())

#csv저장
crawling_date=datetime.datetime.now(timezone('Asia/Seoul')).strftime('%Y%m%d')
#크롤링수집 날짜 저장
youtube_df.to_csv(f'해리포터댓글 수집_{crawling_date}.csv',encoding='utf-8-sig',index=False)

print('='*50)
print('파일저장 완료')

driver.close()














