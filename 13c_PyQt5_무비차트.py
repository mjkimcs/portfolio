# GUI: graphic user interface
# pip install pyqt5
# 구글링 qt designer download - https://build-system.fman.io/qt-designer-download
# 맥 : Designer 탭 - Preferences - Docked window - OK

from PyQt5.QtWidgets import *
from PyQt5 import uic
import sys
import urllib.request as req
from bs4 import BeautifulSoup
from PyQt5.QtGui import QPixmap # GUI 창에 이미지 띄우기

ui_file = "./movie.ui" # Qt Designer에서 미리 창 만들어서 ui파일 저장하기
class MainDialog(QDialog): # 창
    def __init__(self):
        QDialog.__init__(self, None)
        uic.loadUi(ui_file, self)

        self.button.clicked.connect(self.crawling_movie) # Qt Designer에서 objectName

    def crawling_movie(self):

        code = req.urlopen("http://www.cgv.co.kr/movies/")
        soup = BeautifulSoup(code, "html.parser")
        title = soup.select("div.sect-movie-chart strong.title")
        img = soup.select("span.thumb-image > img")

        for i in range(len(title)):

            getattr(self, "txt{}".format(i+1)).setText("{}위 : {}".format(i+1, title[i].string)) # getattr()은 변수라도 문자열 포맷팅을 쓸 수 있게 해주는 함수

            img_url = img[i].attrs["src"]
            img_open = req.urlopen(img_url).read() # 특이한 점
            pixmap = QPixmap()
            pixmap.loadFromData(img_open)
            pixmap = pixmap.scaled(185, 260) # html문서 보면서 이미지 사이즈 조정
            getattr(self, "img{}".format(i+1)).setPixmap(pixmap)


QApplication.setStyle("fusion") # 오류방지
app = QApplication(sys.argv)
main_dialog = MainDialog()
main_dialog.show()
sys.exit(app.exec_())