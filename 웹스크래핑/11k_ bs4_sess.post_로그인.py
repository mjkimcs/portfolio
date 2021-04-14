#로그인이 필요한 사이트에서 BeautifulSoup 사용하여 속도 높이기

#F12 - Network - Preserve log체크 - ALL - 로그인 버튼클릭 - Headers
#get방식: 간편하지만 보안에 취약
#post방식: 보안에 강함

import requests #pip install requests
from bs4 import BeautifulSoup

sess = requests.session() #서버와 나의 연결고리
#Request Headers-Referer & From Data 전체
data = {
"idsave_value":"",
"errorChk":"",
"gourl": "https%3A%2F%2Fwww.donga.com%2Farchive%2Fnewslibrary%2Fview%3Fymd%3D19960210%26mode%3D19960210%2F0002701568%2F1",
"bid": "11lalala",
"bpw": "1234"
}
headers = {"Referer": "https://secure.donga.com/membership/login.php?gourl=https%3A%2F%2Fwww.donga.com%2Farchive%2Fnewslibrary%2Fview%3Fymd%3D19960210%26mode%3D19960210%2F0002701568%2F1"}
sess.post("https://secure.donga.com/membership/trans_exe.php", data=data, headers=headers)

code = sess.get("https://www.donga.com/archive/newslibrary/view?ymd=19960210&mode=19960210/0002701568/1") #urlopen과 같은 기능
soup = BeautifulSoup(code.text, "html.parser")
list = soup.select("ul.news_list a")
for i in list:
    print(i.string)
    content_num = i.attrs["onclick"].replace("javascript:getNewsArticle('19960210/", "").replace("/1'); return false;", "")
    content_url = "https://www.donga.com/archive/newslibrary/view?idx=19960210%2F{}%2F1".format(content_num)
    code = sess.get(content_url) #urlopen과 같은 기능
    soup = BeautifulSoup(code.text, "html.parser") #code.text
    content = soup.select_one("div.article_txt")
    print(content.text)
