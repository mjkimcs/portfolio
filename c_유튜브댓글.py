from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys

b = webdriver.Chrome("./Chromedriver")
b.get("https://www.youtube.com/watch?v=6XP9tIYph_Q&ab_channel=%EB%8D%B0%EC%8B%B8%EB%85%B8%ED%8A%B8")
time.sleep(4)

#send_keys()함수 사용 시 앞에 html요소 아무거나 필요
b.find_element_by_css_selector("html").send_keys(Keys.END)
time.sleep(3)
comments = b.find_elements_by_css_selector("#content-text")
cnt = 0
while True:
    try:
        print(print(comments[cnt].text))
    except:
        print("크롤링 끝!")
        break
    cnt += 1
    if cnt % 15 == 0:
        b.find_element_by_css_selector("html").send_keys(Keys.END)
        time.sleep(3)
        comments = b.find_elements_by_css_selector("#comment #content-text")
b.close()