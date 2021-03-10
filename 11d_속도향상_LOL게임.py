#클릭은 url주소를 찾아내서 urlopen함수를 사용하면 됨

import urllib.request as req
from bs4 import BeautifulSoup #pip install beautifulsoup4

your_champ = input("당신의 챔프>>")
headers = req.Request("https://www.op.gg/champion/statistics", headers={"Accept-Language":"ko-KR"}) #한글로 된 html을 그대로 가져오기
code = req.urlopen(headers)
soup = BeautifulSoup(code, "html.parser")

champ_list = soup.select("div.champion-index__champion-list > div")
for i in champ_list:
    if i.attrs["data-champion-name"] == your_champ:
        a = i.select_one("a")
        champ_url = "https://www.op.gg" + a.attrs["href"]
        break
headers = req.Request(champ_url, headers={"Accept-Language":"ko-KR"}) #한글로 된 html을 그대로 가져오기
code = req.urlopen(headers)
soup = BeautifulSoup(code, "html.parser")
counter_tab = soup.select_one("li.champion-stats-menu__list__item.champion-stats-menu__list__item--red.tabHeader > a")

counter_url = "https://www.op.gg" + counter_tab.attrs["href"]
headers = req.Request(counter_url, headers={"Accept-Language":"ko-KR"}) #한글로 된 html을 그대로 가져오기
code = req.urlopen(headers)
soup = BeautifulSoup(code, "html.parser")
counter = soup.select("div.champion-matchup-list__champion > span:nth-child(2)")
for i in counter:
    print(i.string)