#iframe 프레임전환
#:nth-child()

from selenium import webdriver
import time
import pyperclip  # pip install pyperclip
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys


def input_id_pw(b, css, user_input):
    pyperclip.copy(user_input)
    b.find_element_by_css_selector(css).click()
    ActionChains(b).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()


option = webdriver.ChromeOptions()
b = webdriver.Chrome("./chromedriver", options=option)  # , options=option
b.get("https://nid.naver.com/nidlogin.login?mode=form&url=https%3A%2F%2Fwww.naver.com")

input_id_pw(b, "#id", "11lalala")
time.sleep(1)
input_id_pw(b, "#pw", "1234")
time.sleep(1)
b.find_element_by_css_selector("input.btn_global").click()
time.sleep(3)

b.get("https://cafe.naver.com/joonggonara")
time.sleep(3)

tab = b.find_elements_by_css_selector("h3 > a.gm-tcol-t.ellipsis")
tab_c = tab[1].click() #우리동네 서울 클릭
time.sleep(2)

tab = b.find_elements_by_css_selector("ul#group1708 li > a")
tab_c = tab[5].click() #우리동네 양천구 클릭
time.sleep(2)

try:
    f = open("./중고나라.txt", "r", encoding='UTF-8')
    hist = f.readlines()
except:
    f = open("./중고나라.txt", "w", encoding='UTF-8')
    hist = []

b.switch_to.frame(b.find_element_by_css_selector("iframe#cafe_main"))
title = b.find_elements_by_css_selector("div#main-area > div.article-board.m-tcol-c:nth-child(6) div.board-list a.article") #:nth-child()
new_one = 0
for i in title:
    if not (i.text + "\n") in hist: #최신 글이라면
        f = open("./중고나라.txt", "a", encoding='UTF-8')
        f.write(i.text + "\n")
        if "스타벅스" in i.text:
            new_one += 1
f.close()
print("{}관련 글이 {}개 올라왔다.".format("스타벅스", new_one))
b.close()

#www.twilio.com

import os
from twilio.rest import Client #모듈이 설치되어 있지 않아 빨간줄이 생길경우 커서를 놓고 alt+Enter+Enter

if new_one >=1:
    account_sid = os.environ['AC49c08f671a79f08b697304a6753574b0']
    auth_token = os.environ['ee9420e37eb1719a3cb745feb3c9ccaa']
    client = Client(account_sid, auth_token)

    message = client.messages \
                    .create(
                         body="{}관련 글이 {}개 올라왔다. https://cafe.naver.com/joonggonara".format("의자", new_one),
                         from_='+15107562106',
                         to='+821026759201'
                     )
