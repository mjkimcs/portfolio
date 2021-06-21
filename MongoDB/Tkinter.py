import tkinter
import tkinter.font
import tkinter.ttk
from tkinter.scrolledtext import ScrolledText
from tkinter import *
from ScrapingToFIle import ScrapingToFile
import FileToOracle
import OracleToMongoDB


class Tkinter:
    def GUI(self):
        self.window = tkinter.Tk()  # tkinter창
        self.window.title("영화리뷰")
        self.window.geometry("820x720+100+100")
        self.window.resizable(False, False)  # 윈도우 창크기 조절 가능
        # 이미지
        image = tkinter.PhotoImage(file="Supports/영아박스.png")
        img_label = tkinter.Label(self.window, image=image)
        img_label.place(x=280, y=-10, width=300, height=100)
        # 영화검색창 디자인
        # 검색창 폰트크기
        font1 = tkinter.font.Font(size=20, weight="bold")
        label = tkinter.Label(self.window, text="영화제목 :", font=font1)  # 영화검색
        label.place(x=120, y=90)
        # super_name_box.insert(0, self.__super_name)
        self.__sv_super_name_box = StringVar()
        self.__sv_super_name_box.trace("w", lambda name, index, mode,
                                                   buffer=self.__sv_super_name_box: self.__Entry_value_changed(
            self.__sv_super_name_box))
        super_name_box = tkinter.Entry(self.window, bg="white", textvariable=self.__sv_super_name_box,
                                       width=37)  # 이후 크롤링 제목에 들어갈 부분
        super_name_box.place(x=280, y=95, width=300, height=30)
        b1 = tkinter.Button(self.window, text="검색", font=font1, command=self.__Scraping)  # 버튼의 위치, command로 아래 화면이 나오게 연결
        b1.place(x=600, y=93, width=55, height=30)
        # 아래 크롤링이 나오는 부분
        frame3 = tkinter.Frame(self.window, bd=1, highlightthickness=1, highlightbackground="purple")
        frame3.place(x=15, y=530, width=790, height=178)
        # frame3.pack(fill="both", expand="yes", padx=10, pady=2)
        self.__frame3_scrollbar = ScrolledText(frame3, height=0)
        self.__frame3_scrollbar.pack(side=tkinter.LEFT, fill="both", expand="yes")

        self.first_trv()

        star_btn = tkinter.Button(self.window, text="별점별", font=font1, command=self.__test01)
        star_btn.place(x=120, y=135, width=110, height=35)
        date_btn = tkinter.Button(self.window, text="날짜별", font=font1, command=self.__test02)
        date_btn.place(x=260, y=135, width=110, height=35)
        sympathy_btn = tkinter.Button(self.window, text="분위기별", font=font1, command=self.__test03)
        sympathy_btn.place(x=410, y=135, width=110, height=35)
        sympathy_btn = tkinter.Button(self.window, text="한줄평", font=font1, command=self.__test04)
        sympathy_btn.place(x=550, y=135, width=110, height=35)
        self.window.mainloop()  # 윈도우창 끌때 멈춰라

    def first_trv(self):
        frame = tkinter.Frame(self.window, bd=1, highlightthickness=1, highlightbackground="#57E9E1")  # 배경색, 테두리
        frame.place(x=15, y=180, width=790, height=340)
        self.__trv = tkinter.ttk.Treeview(frame, columns=["1", "2", "3", "4", "5", "6"])
        self.__trv.place(width=785, height=335)
        # 컬럼명과 폭을 지정
        self.__trv.column("#0", width=1)
        self.__trv.column("1", width=20)
        self.__trv.heading("1", text="평점")
        self.__trv.column("2", width=300)
        self.__trv.heading("2", text="한줄평")
        self.__trv.column("3", width=80)
        self.__trv.heading("3", text="날짜")
        self.__trv.column("4", width=80)
        self.__trv.heading("4", text="좋아요")
        self.__trv.column("5", width=80)
        self.__trv.heading("5", text="싫어요")
        self.__trv.column("6", width=80)
        self.__trv.heading("6", text="분위기")
        self.__trv.bind('<Button-1>', self.__Select_row)

    def __test01(self):
        self.__trv.destroy()
        # 트리뷰로 행과 열로 구성된 표를 만들자
        frame01 = tkinter.Frame(bd=1, highlightthickness=1, highlightbackground="#57E9E1")  # 배경색, 테두리
        frame01.place(x=15, y=180, width=790, height=340)
        self.__trv = tkinter.ttk.Treeview(frame01, columns=["1", "2", "3", "4", "5", "6", "7", "8"])
        self.__trv.place(width=785, height=335)
        # 스크롤바
        sb = Scrollbar(self.__trv, orient=VERTICAL)
        sb.pack(side=RIGHT, fill=Y)
        self.__trv.config(yscrollcommand=sb.set)
        sb.config(command=self.__trv.yview)
        # 컬럼명과 폭을 지정
        self.__trv.column("#0", width=1)
        self.__trv.column("1", width=20)
        self.__trv.heading("1", text="별점")
        self.__trv.column("2", width=40)
        self.__trv.heading("2", text="게시글 수")
        self.__trv.column("3", width=70)
        self.__trv.heading("3", text="좋아요 수")
        self.__trv.column("4", width=70)
        self.__trv.heading("4", text="싫어요 수")
        self.__trv.column("5", width=95)
        self.__trv.heading("5", text="긍정 수")
        self.__trv.column("6", width=95)
        self.__trv.heading("6", text="부정 수")
        self.__trv.column("7", width=95)
        self.__trv.heading("7", text="긍정 비율")
        self.__trv.column("8", width=95)
        self.__trv.heading("8", text="부정 비율")
        self.__trv.bind('<Button-1>', self.__Select_row)

        data = OracleToMongoDB.OracleToMongoDB().star()
        for i in range(len(data)):
            self.__trv.insert('', 'end', values=data[i])

        self.window.geometry("820x530")

    def __test02(self):
        self.__trv.destroy()
        # 트리뷰로 행과 열로 구성된 표를 만들자
        frame01 = tkinter.Frame(bd=1, highlightthickness=1, highlightbackground="#57E9E1")  # 배경색, 테두리
        frame01.place(x=15, y=180, width=790, height=340)
        self.__trv = tkinter.ttk.Treeview(frame01, columns=["1", "2", "3", "4", "5", "6", "7", "8", "9"])
        self.__trv.place(width=785, height=335)
        # 스크롤바
        sb = Scrollbar(self.__trv, orient=VERTICAL)
        sb.pack(side=RIGHT, fill=Y)
        self.__trv.config(yscrollcommand=sb.set)
        sb.config(command=self.__trv.yview)
        # 컬럼명과 폭을 지정
        self.__trv.column("#0", width=1)
        self.__trv.column("1", width=70)
        self.__trv.heading("1", text="날짜")
        self.__trv.column("2", width=70)
        self.__trv.heading("2", text="게시글 수")
        self.__trv.column("3", width=65)
        self.__trv.heading("3", text="좋아요 수")
        self.__trv.column("4", width=65)
        self.__trv.heading("4", text="싫어요 수")
        self.__trv.column("5", width=65)
        self.__trv.heading("5", text="긍정 수")
        self.__trv.column("6", width=65)
        self.__trv.heading("6", text="부정 수")
        self.__trv.column("7", width=65)
        self.__trv.heading("7", text="긍정비율")
        self.__trv.column("8", width=65)
        self.__trv.heading("8", text="부정비율")
        self.__trv.column("9", width=75)
        self.__trv.heading("9", text="별점 평균")
        self.__trv.bind('<Button-1>', self.__Select_row)

        data = OracleToMongoDB.OracleToMongoDB().date()
        for i in range(len(data)):
            self.__trv.insert('', 'end', values=data[i])

        self.window.geometry("820x530")

    def __test03(self):
        self.__trv.destroy()
        # 트리뷰로 행과 열로 구성된 표를 만들자
        frame01 = tkinter.Frame(bd=1, highlightthickness=1, highlightbackground="#57E9E1")  # 배경색, 테두리
        frame01.place(x=15, y=180, width=790, height=340)
        self.__trv = tkinter.ttk.Treeview(frame01, columns=["1", "2", "3", "4", "5"])
        self.__trv.place(width=785, height=335)
        # 스크롤바
        sb = Scrollbar(self.__trv, orient=VERTICAL)
        sb.pack(side=RIGHT, fill=Y)
        self.__trv.config(yscrollcommand=sb.set)
        sb.config(command=self.__trv.yview)
        # 컬럼명과 폭을 지정
        self.__trv.column("#0", width=1)
        self.__trv.column("1", width=90)
        self.__trv.heading("1", text="분위기")
        self.__trv.column("2", width=90)
        self.__trv.heading("2", text="사람 수")
        self.__trv.column("3", width=110)
        self.__trv.heading("3", text="좋아요 수")
        self.__trv.column("4", width=110)
        self.__trv.heading("4", text="싫어요 수")
        self.__trv.column("5", width=110)
        self.__trv.heading("5", text="별점평균")
        self.__trv.bind('<Button-1>', self.__Select_row)

        data = OracleToMongoDB.OracleToMongoDB().sympathy()
        for i in range(len(data)):
            self.__trv.insert('', 'end', values=data[i])

        self.window.geometry("820x530")

    def __test04(self):
        self.__trv.destroy()

        frame01 = tkinter.Frame(bd=1, highlightthickness=1, highlightbackground="#57E9E1")  # 배경색, 테두리
        frame01.place(x=15, y=180, width=790, height=340)
        self.__trv = tkinter.ttk.Treeview(frame01, columns=["1", "2", "3", "4", "5", "6"])
        self.__trv.place(width=785, height=335)
        # 스크롤바
        sb = Scrollbar(self.__trv, orient=VERTICAL)
        sb.pack(side=RIGHT, fill=Y)
        self.__trv.config(yscrollcommand=sb.set)
        sb.config(command=self.__trv.yview)

        # 컬럼명과 폭을 지정
        self.__trv.column("#0", width=1)
        self.__trv.column("1", width=20)
        self.__trv.heading("1", text="평점")
        self.__trv.column("2", width=350)
        self.__trv.heading("2", text="한줄평")
        self.__trv.column("3", width=80)
        self.__trv.heading("3", text="날짜")
        self.__trv.column("4", width=80)
        self.__trv.heading("4", text="좋아요")
        self.__trv.column("5", width=80)
        self.__trv.heading("5", text="싫어요")
        self.__trv.column("6", width=80)
        self.__trv.heading("6", text="분위기")

        self.__trv.bind('<Button-1>', self.__Select_row)

        data = OracleToMongoDB.OracleToMongoDB().normal()
        for i in range(len(data)):
            self.__trv.insert('', 'end', values=data[i])

        self.window.geometry("820x720")

    def __Scraping(self):
        scrapingToFile = ScrapingToFile()
        __title = scrapingToFile.Web_scraping(self.__super_name)
        if __title is not None:
            FileToOracle.FileToOracle(__title)
            if OracleToMongoDB.OracleToMongoDB().Morpheme(__title):
                self.__test04()

    def __Select_row(self, event):
        rowid = self.__trv.identify_row(event.y)  # rowid는 오라클의 rowid가 아니라 tkinter에서 제공하는 트리뷰 row의 고유번호를 의미한다.
        if rowid is not "":
            row_info = self.__trv.set(rowid)
            # 기존의 scrollbar안의 텍스트를 삭제하고, 새로 선택된 행의 콤보박스에 선택된 컬럼의 값을 scrollbar에 넣어준다.
            self.__frame3_scrollbar.delete('1.0', END)
            self.__frame3_scrollbar.insert(tkinter.INSERT, row_info[str(2)])

    def __Entry_value_changed(self, buffer):
        self.__super_name = buffer.get()


if __name__ == '__main__':
    Tkinter().GUI()
