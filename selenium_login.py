from selenium import webdriver
import time

browser = webdriver.Chrome()
browser.get("https://naver.com/")

elem = browser.find_element_by_class_name("link_login")
elem.click()

browser.find_element_by_id("id").send_keys("lalala")
browser.find_element_by_id("pw").send_keys("min")
browser.find_element_by_id("log.login").click()

time.sleep(1)
browser.find_element_by_id("id").clear()
browser.find_element_by_id("id").send_keys("11lalala")

print(browser.page_source)

browser.quit()