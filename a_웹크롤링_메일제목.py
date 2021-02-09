#pip install selenium
#ChromeDriver 버전확인 앞2자리: 점3개-도움말-크롬정보

from selenium import webdriver
import time
b = webdriver.Chrome("./chromedriver")
b.get("https://logins.daum.net/accounts/signinform.do?url=https%3A%2F%2Fwww.daum.net%2F")
id = b.find_element_by_css_selector("input#id")
id.send_keys("11lalala")
pw = b.find_element_by_css_selector("input#inputPwd")
pw.send_keys("1234")
b.find_element_by_css_selector(("button#loginBtn")).click()
time.sleep(3)

b.get("https://mail.daum.net/")
time.sleep(2)
title = b.find_elements_by_css_selector("strong.tit_subject")
for i in title:
    print(i.text)
b.close()
