# GUI: graphic user interface
# pip install pyqt5
# 구글링 qt designer download - https://build-system.fman.io/qt-designer-download
# 맥 : Designer 탭 - Preferences - Docked window - OK

from PyQt5.QtWidgets import *
from PyQt5 import uic
import sys
import math  # inputbox에 math.sin(100)을 입력하면 계산해줌


ui_file = "./calculator.ui"
class MainDialog(QDialog): # 창
    def __init__(self):
        QDialog.__init__(self, None)
        uic.loadUi(ui_file, self)

        self.equalbutton.clicked.connect(self.calculate) #Qt Designer에서 objectName

    def calculate(self):
        equation = self.inputbox.text() #text함수는 lineEdit에 쓴 텍스트를 읽어옴
        result = eval(equation)
        history_text = "{}\n= {}\n".format(equation, result)
        self.history.append(str(history_text))


QApplication.setStyle("fusion")
app = QApplication(sys.argv)
main_dialog = MainDialog()
main_dialog.show()
sys.exit(app.exec_())
