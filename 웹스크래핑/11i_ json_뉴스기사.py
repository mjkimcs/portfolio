#BeautifulSoup으로 크롤링이 안 될 경우

#요청(request): 클라이언트 -> 서버
#GET 요청방식: url에 표시, 빠른속도, 보안취약, 대용량데이터 불가능
#POST 요청방식: 보안강함, 대용량데이터 가능
#Network - Preserve log - All
#빨간색은 무시
#clear 아이콘 - 새로고침
#대부분 Doc 또는 XHR

import urllib.request as req
from bs4 import BeautifulSoup
import urllib.parse as par
import requests
import json

keyword = ["IT", "코딩", "자동화"]

pg_num = 0
for i in keyword:
    encoded = par.quote(i) #한글->특수한 문자
    while True:
        url ="https://www.chosun.com/pf/api/v3/content/fetch/search-param-api" #Network탭 Preview에 내용이 있으면 Headers에서 물음표 앞까지만 url 복사
        #format함수는 중괄호와 짝이 맞으니 컴퓨터가 헷갈리지 않게 중괄호 2번쓰기
        params = {
        "query" : '{{"date_period":"all","emd_word":"","encodeURI":"true","expt_word":"","field":"","page":{},"query":"{}","siteid":"","sort":"1","writer":""}}'.format(pg_num, encoded),
        "d" : "383",
        "_website" : "chosun"
        } #Query String Parameters 복사
        result = requests.get(url, params=params)
        result = json.loads(result.text) #json->딕셔너리 자료형
        news = result["content_elements"]
        if len(news) == 0:
            print("크롤링 끝!")
            break
        for i in news:
            print("제목: ", i["title"])
            print("본문: ", i["body"])
            print()
        pg_num += 1
