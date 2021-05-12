# 점3개 - 설정 - Chrome정보
# https://chromedriver.chromium.org/downloads


from bs4 import BeautifulSoup
import urllib.request
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import time


def Test():
    b = webdriver.Chrome("./chromedriver.exe")
    b.get("https://www.google.com/imghp?tbm=isch&tab=wi&ei=l1AdWbegOcra8QXvtr-4Cw&sclient=img&ved=0ahUKEwjvxonUvMPwAhWRZd4KHd7aAQUQ4dUDCAc&uac")

    elem = b.find_element_by_class_name("gLFyf.gsfi")
    elem.send_keys("사과")
    elem.submit()

    for i in range(1,2):
        b.find_element_by_xpath("//body").send_keys(Keys.END)
        time.sleep(3)

    result = b.page_source
    soup = BeautifulSoup(result, "lxml")
    print(soup.find_all("img", class_="rg_i Q4LuWd"))
    return soup


def fetch_list_url():
    soup = Test()
    imgList = soup.find_all("img", class_="rg_i Q4LuWd")
    params = []
    for i in imgList:
        try:
            params.append(i["src"])
        except KeyError:
            params.append(i["data-src"])
    return params


def fetch_detail_url():
    params = fetch_list_url()
    for i, j in enumerate (params, 1):
        urllib.request.urlretrieve(j, "c:/Test_img/" + str(i) + "_google.jpg")


if __name__ == '__main__':
    fetch_detail_url()