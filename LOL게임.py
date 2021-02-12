#op.gg
from selenium import webdriver
import time

his_champ = input("상대 챔프>>")
b = webdriver.Chrome("./chromedriver")
b.get("https://www.op.gg/champion/statistics")
time.sleep(3)

champs = b.find_elements_by_css_selector("div.champion-index__champion-item__name")
for i in champs:
    if i.text == his_champ:
        i.click()
        break
time.sleep(3)

b.find_element_by_css_selector("li.champion-stats-menu__list__item.champion-stats-menu__list__item--red.tabHeader > a").click()
time.sleep(2)

counter = b.find_elements_by_css_selector("div.champion-matchup-list__champion > span:nth-child(2)")
for i in counter:
    print(i.text)
b.close()

