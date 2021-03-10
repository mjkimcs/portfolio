from selenium import webdriver
import time

b= webdriver.Chrome("./chromedriver")
b.get("https://logins.daum.net/accounts/signinform.do?url=https%3A%2F%2Fwww.daum.net%2F")

id = b.find_element_by_css_selector("#id")
id.send_keys("11lalala")
pw = b.find_element_by_css_selector("#inputPwd")
pw.send_keys("1234")
b.find_element_by_css_selector("#loginBtn").click()
time.sleep(3)

b.get("https://cafe.daum.net/2minkim")
time.sleep(3)

b.switch_to.frame(b.find_element_by_css_selector("iframe#down")) #한 화면에 여러개의 웹페이지가 있기 때문에 프레임 전환
b.find_element_by_css_selector("#fldlink_lF1R_309").click() #가입인사 클릭
time.sleep(3)

b.find_element_by_css_selector("#article-write-btn").click() #글쓰기 클릭
time.sleep(3)

subject = b.find_element_by_css_selector("#title-input")
subject.send_keys("안녕하세요!") #제목 작성

b.switch_to.frame(b.find_element_by_css_selector("#keditorContainer_ifr")) #프레임 전환
content = b.find_element_by_css_selector("#tinymce")
content.send_keys("반갑습니다.") #본문 작성

b.switch_to.default_content() #프레임 전환은 바깥에서 안쪽으로만 가능하기 때문에 제일 바깥으로 우선 빠져 나가기
b.switch_to.frame(b.find_element_by_css_selector("#down")) #프레임 전환
b.find_element_by_css_selector(".btn_g.full_type1").click() #등록 클릭
time.sleep(3)
b.close()