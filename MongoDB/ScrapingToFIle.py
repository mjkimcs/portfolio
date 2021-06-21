import os
from bs4 import BeautifulSoup
from selenium import webdriver
from tkinter import messagebox
import urllib.request as req
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time


class ScrapingToFile:
    def Web_scraping(self, super_name):
        b = webdriver.Chrome("./chromedriver.exe")  # , options=option
        b.get("https://movie.naver.com/movie/point/af/list.nhn")
        search_box = b.find_element_by_css_selector("span.ipt_srch input")

        search_box.send_keys(super_name)

        b.find_element_by_css_selector("div.srch_field_on._view button").click()
        time.sleep(2)

        while True:
            if "code" in b.current_url:
                break

        __title_val = b.find_element_by_css_selector("#content > div.article > div.mv_info_area > "
                                                     "div.mv_info > h3 > a:nth-child(1)").get_attribute(
            "text").replace(":", "")

        folder_path = "Original_data"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        self.path = folder_path + "/" + __title_val + ".csv"
        if os.path.exists(self.path):
            if messagebox.askyesno("확인", "같은 데이터가 이미 존재합니다. 기존 데이터를 삭제하고 새로 만드시겠습니까?"):
                if os.path.exists(self.path):
                    os.remove(self.path)
            else:
                b.quit()
                return None

        star_score = []
        contents = []
        reg_date = []
        sympathy = []
        not_sympathy = []
        try:
            b.find_element_by_css_selector("div.score  a.link_more").click()
            val = b.find_element_by_css_selector("div#content input").get_attribute("value")

            page_num = 1
            while True:
                code = req.urlopen(
                    "https://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn?code={"
                    "}&type=after&isActualPointWriteExecute=false&isMileageSubscriptionAlready=false"
                    "&isMileageSubscriptionReject=false&page={}".format(
                        val, page_num))
                soup = BeautifulSoup(code, "html.parser")

                star_score_val = soup.select("div.score_result > ul > li > div.star_score > em")
                for i in star_score_val:
                    star_score.append(i.text)
                contents_val = soup.select("li > div.score_reple > p > span")
                if contents_val[-1].text.strip() == "":
                    break
                for i in contents_val:
                    i = i.text.strip()
                    if i == "관람객":
                        continue
                    contents.append(i)
                reg_date_val = soup.select("body > div > div > div.score_result > ul > li > div.score_reple > "
                                           "dl > dt > em:nth-of-type(2)")
                for i in reg_date_val:
                    reg_date.append(i.text)
                sympathy_val = soup.select("body > div > div > div.score_result > ul > li > div.btn_area > "
                                           "a._sympathyButton > strong")
                for i in sympathy_val:
                    sympathy.append(i.text)
                not_sympathy_val = soup.select("body > div > div > div.score_result > ul > li > div.btn_area > "
                                               "a._notSympathyButton > strong")
                for i in not_sympathy_val:
                    not_sympathy.append(i.text)
                page_num += 1
                try:
                    url = 'https://movie.naver.com' + soup.find('a', {'class': 'pg_next'}).get('href')
                except:
                    break
        except:
            messagebox.showerror("", "해당 작품의 리뷰가 존재하지 않습니다.")
            b.quit()
            return None

        # self.path : Original_data + "/" + super_name + ".csv"
        f = open(self.path, "w", encoding='utf-8')
        f.write("별점, 내용, 날짜, 좋아요, 싫어요\n")
        for star, con, reg, sym, not_sym in zip(star_score, contents, reg_date, sympathy, not_sympathy):
            f.write("" + star + ", '" + con.replace('\'', '')
                    + "', '" + reg[0:10] + "', " + sym + ", " + not_sym + "\n")
        f.close()
        b.quit()
        return __title_val