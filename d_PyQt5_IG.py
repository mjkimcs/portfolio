# GUI: graphic user interface
# pip install pyqt5
# 구글링 qt designer download - https://build-system.fman.io/qt-designer-download
# 맥 : Designer 탭 - Preferences - Docked window - OK



# [ Worker1이 Worker2에게 신호를 보내는 경우 ]
# 1. (Worker1 공간)신호를 정의 ex)login_signal = pyqtSignal()
# 2. (Worker1 공간)Worker2에게 신호 보내기 ex)self.login_signal.connect(self.worker.login)
# 3. (Worker2 공간)login함수 실행
#
# [ Worker2가 Worker1에게 신호를 보내는 경우 ] 1탄
# 1. (Worker2 공간)신호를 정의 ex)login_progress_signal = pyqtsignal(int)
# 2. (Worker2 공간)Worker1에게 신호 보내기 ex)self.login_progress_signal.emit(10)
# 3. (Worker1 공간)Worker1이 신호를 받기 ex)self.worker.login_progress_signal.connect(self.login_progress.setValue)
# 4. (Worker1 공간)login_progress 초기값 설정하기 ex)self.login_progress.setValue(0)
#
# [ Worker2가 Worker1에게 신호를 보내는 경우 ] 2탄
# 1. (Worker2 공간)신호를 정의 ex)content_signal = pyqtsignal(str)
# 2. (Worker2 공간)Worker1에게 신호 보내기 ex)self.content_signal.emit(content.text)
# 3. (Worker1 공간)Worker1이 신호를 받기 ex)self.worker.content_signal.connect(self.show_content)
# 4. (Worker1 공간)show_content함수 정의하기 ex)def show_content(self, data): self.txt.setText(data)



from PyQt5.QtWidgets import *
from PyQt5 import uic
import sys
import os
from selenium import webdriver
import time
from PyQt5.QtCore import QObject, QThread, pyqtSignal # Worker2 생성
import random
import urllib.request as req # 이미지
from PyQt5.QtGui import QPixmap # 이미지

ui_file = "./ig.ui"

class SeleniumWorker(QObject): # Selenium 동작만을 위한 Worker2 생성
    login_progress_signal = pyqtSignal(int) # Worker1에게 진행정도를 보내주는 기반작업
    login_success_signal = pyqtSignal(bool)
    search_progress_signal = pyqtSignal(int)
    search_success_signal = pyqtSignal(bool)
    img_signal = pyqtSignal(str)
    content_signal = pyqtSignal(str)
    def __init__(self):
        self.b = webdriver.Chrome("./chromedriver") # init함수에서 만들어진 변수는 특이하게도 전역변수로 사용가능
        QObject.__init__(self, None)
        self.user_id = ""
        self.user_pw = ""
        self.user_keyword = ""

    def login(self):
        # b = webdriver.Chrome("./chromedriver") # 함수 안에 있는 변수는 지역변수라서 코딩하기 어려우므로 밖으로 빼줌(위쪽 확인)
        self.b.get("https://www.instagram.com/accounts/login/?source=auth_switcher")
        self.login_progress_signal.emit(10) # Worker1에게 시그널 보내기
        time.sleep(3)
        self.login_progress_signal.emit(20) # Worker1에게 시그널 보내기
        id = self.b.find_element_by_name("username")
        id.send_keys(self.user_id)
        self.login_progress_signal.emit(40)
        pw = self.b.find_element_by_name("password")
        pw.send_keys(self.user_pw)
        self.login_progress_signal.emit(60)
        self.b.find_element_by_css_selector("div.Igw0E.IwRSH.eGOV_._4EzTm.bkEs3.CovQj.jKUp7.DhRcB").click()
        self.login_progress_signal.emit(80)
        time.sleep(3)
        self.login_progress_signal.emit(100)
        if self.b.current_url == "https://www.instagram.com/accounts/onetap/?next=%2F":
            self.login_success_signal.emit(True)
        else:
            self.login_success_signal.emit(False)

    def search(self):
        self.search_progress_signal.emit(20)
        url = "https://www.instagram.com/explore/tags/{}/".format(self.user_keyword)
        self.b.get(url)
        self.search_progress_signal.emit(40)
        time.sleep(7)
        self.search_progress_signal.emit(60)
        self.b.find_element_by_css_selector("div._9AhH0").click()
        self.search_progress_signal.emit(80)
        time.sleep(3)
        self.search_progress_signal.emit(100) # emit의 목적지를 지정해줘야 하므로 Worker1으로 이동
        self.search_success_signal.emit(True)
        row_num = 1
        while True:
            like = self.b.find_element_by_css_selector("section.ltpMr.Slqrh button.wpO6b svg._8-yf5")
            value = like.get_attribute("aria-label")
            next = self.b.find_element_by_css_selector("a._65Bje.coreSpriteRightPaginationArrow")
            img = self.b.find_element_by_css_selector("article.M9sTE.L_LMM.JyscU.ePUX4 img.FFVAD")
            content = self.b.find_element_by_css_selector("div.C4VMK > span")
            self.content_signal.emit(content.text)
            self.img_signal.emit(img.get_attribute("src"))
            if value == "좋아요":  # 좋아요가 안 눌려져 있다면
                like.click()
                time.sleep(random.randint(2, 5) + random.random())  # 인스타그램을 속이기 위한 랜덤한 소수
                next.click()
                time.sleep(random.randint(2, 5) + random.random())
            elif value == "좋아요 취소":  # 좋아요가 눌려져 있다면
                next.click()
                time.sleep(random.randint(2, 5) + random.random())



class MainDialog(QDialog): # Worker1 창 관리
    login_signal = pyqtSignal() # Worker2에게 신호를 보내기 위한 기반작업
    search_signal = pyqtSignal()
    def __init__(self):
        QDialog.__init__(self, None)
        uic.loadUi(ui_file, self)

        self.worker = SeleniumWorker() # Worker2를 작업공간에 배치
        self.thread = QThread() # 작업공간 만들어주기
        self.worker.moveToThread(self.thread)
        self.thread.start() # Worker2를 작업공간에 배치 시작

        self.button_search.setEnabled(False)
        self.login_progress.setValue(0)
        self.search_progress.setValue(0)

        self.button_login.clicked.connect(self.login_start)

        self.login_signal.connect(self.worker.login) # Worker2에게 신호를 보내기
        self.worker.login_progress_signal.connect(self.login_progress.setValue) # Worker2가 신호를 보내는 것을 받기
        self.worker.login_success_signal.connect(self.finish_login)

        self.button_search.clicked.connect(self.search_start)

        self.search_signal.connect(self.worker.search)
        self.worker.search_progress_signal.connect(self.search_progress.setValue)
        self.worker.search_success_signal.connect(self.finish_search)
        self.worker.content_signal.connect(self.show_content)
        self.worker.img_signal.connect(self.show_img)

    def login_start(self):
        self.login_status.setText("로그인 중...")
        self.button_login.setEnabled(False) # 로그인 버튼 한 번만 누른 후 비활성화
        self.worker.user_id = self.input_id.text()
        self.worker.user_pw = self.input_pw.text()
        self.login_signal.emit() # Worker2에게 신호를 보내기
        # user_id = self.input_id.text()
        # user_pw = self.input_pw.text()

    def finish_login(self, data):
        if data == True:
            self.login_status.setText("로그인 성공!")
            self.button_search.setEnabled(True)
        else:
            self.login_status.setText("로그인 실패! 다시 시도")
            self.button_login.setEnabled(True)

    def search_start(self):
        self.search_status.setText("해시태그 검색 중...")
        self.button_search.setEnabled(False)
        self.worker.user_keyword = self.input_hash.text()
        self.search_signal.emit() # Worker2에게 신호를 보내기

    def finish_search(self, data):
        if data == True:
            self.search_status.setText("자동 좋아요 누르는 중...")

    def show_img(self, data): # 이미지 창에 띄우기
        d = req.urlopen(data).read()
        pixmap = QPixmap()
        pixmap.loadFromData(d)
        pixmap = pixmap.scaled(250, 250)
        self.img.setPixmap(pixmap)

    def show_content(self, data):
        self.txt.setText(data)



QApplication.setStyle("fusion") # 오류방지
app = QApplication(sys.argv)
main_dialog = MainDialog()
main_dialog.show()
sys.exit(app.exec_())
