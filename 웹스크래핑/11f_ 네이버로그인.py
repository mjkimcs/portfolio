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
# option.add_argument("headless")
b = webdriver.Chrome("./chromedriver") #, options=option
b.get("https://nid.naver.com/nidlogin.login?mode=form&url=https%3A%2F%2Fwww.naver.com")

input_id_pw(b, "#id", "11lalala")
time.sleep(1)
input_id_pw(b, "#pw", "1234")
time.sleep(1)
b.find_element_by_css_selector("input.btn_global").click()
time.sleep(3)

b.get("https://mail.naver.com/")
time.sleep(3)
title = b.find_elements_by_css_selector("strong.mail_title")
for i in title:
    print(i.text)
b.close()
