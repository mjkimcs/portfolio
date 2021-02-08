from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

browser = webdriver.Chrome()
browser.maximize_window()

url = "https://flight.naver.com/flights/"
browser.get(url)

browser.find_element_by_link_text("가는날 선택").click()
browser.find_elements_by_link_text("28")[0].click()
browser.find_elements_by_link_text("5")[1].click()

browser.find_element_by_xpath("//*[@id='recommendationList']/ul/li[1]").click()

browser.find_element_by_link_text("항공권 검색").click()

try:
    elem = WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//*[@id='content']/div[2]/div/div[4]/ul/li[1]")))
    print(elem[0].text)
finally:
    browser.quit()

# elem = browser.find_element_by_xpath("//*[@id='content']/div[2]/div/div[4]/ul/li[1]")
# print(elem.text)
