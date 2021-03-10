# GUI: graphic user interface
# pip install pyqt5
# 구글링 qt designer download - https://build-system.fman.io/qt-designer-download
# 맥 : Designer 탭 - Preferences - Docked window - OK

from PyQt5.QtWidgets import *
from PyQt5 import uic
import sys

ui_file = "./movie.ui" # Qt Designer에서 미리 창 만들어서 ui파일 저장하기
class MainDialog(QDialog): # 창
    def __init__(self):
        QDialog.__init__(self, None)
        uic.loadUi(ui_file, self)

        self.pushButton.clicked.connect(self.buttonClicked) # Qt Designer에서 objectName

    def buttonClicked(self):
        result = self.lineEdit.text() # text()는 lineEdit에 쓴 텍스트를 읽어옴
        self.label.setText(result)

QApplication.setStyle("fusion") # 오류방지
app = QApplication(sys.argv)
main_dialog = MainDialog()
main_dialog.show()
sys.exit(app.exec_())