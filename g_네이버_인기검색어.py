import requests #pip install requests
import urllib.request as req
from bs4 import BeautifulSoup
import urllib.parse as par

json = requests.get("https://www.naver.com/srchrank?frm=main").json()
ranks = json.get("data")
for i in range(20):
    print("{}. ".format(i+1) + ranks[i]["keyword"])

    url = "https://search.naver.com/search.naver?where=news&sm=tab_jum&query="
    keyword = par.quote(ranks[i]["keyword"]) #한글->특수한 문자
    url_result = url + keyword
    code= req.urlopen(url_result)
    soup = BeautifulSoup(code, "html.parser")
    news = soup.select(".news_tit")
    for n in news[:3]:
        print("관련기사: ", n.text)