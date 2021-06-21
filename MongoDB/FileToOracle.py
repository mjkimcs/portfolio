import csv
import cx_Oracle
from tkinter import messagebox
import os


class FileToOracle:
    def __init__(self, super_name):
        self.__super_name = super_name

        dsn = cx_Oracle.makedsn("localhost", 1521, 'xe')
        self.__db = cx_Oracle.connect('SCOTT', 'TIGER', dsn)
        self.__cur = self.__db.cursor()

        self.__Create_table()

    def __del__(self):
        self.__cur.close()
        self.__db.close()

    def __Create_table(self):
        self.__cur.execute("SELECT COUNT(*) FROM ALL_TABLES WHERE TABLE_NAME = '" + self.__super_name.upper() + "'")
        if self.__cur.fetchone()[0] == 1:
            query = "DROP TABLE \"" + self.__super_name + "\""
            self.__cur.execute(query)

        path = "Original_data/" + self.__super_name + ".csv"
        if os.path.exists(path):
            f = open(path, 'r', encoding='utf-8')
            csv_reader = csv.reader(f)
            headers = next(csv_reader)
            rows = next(csv_reader)
            header_name = ''
            for header, row in zip(headers, rows):
                if row.strip().isdigit():
                    header_name += header + ' NUMBER,'
                else:
                    header_name += header + ' VARCHAR2(4000),'
            query = "CREATE TABLE \"" + self.__super_name + "\""\
                    "(" \
                    + header_name.rstrip(',') + \
                    ")"
            self.__cur.execute(query)
            self.__Insert(path)
        else:
            messagebox.showerror("", "csv파일이 존재하지 않습니다.")

    def __Insert(self, path):
        f = open(path, 'r', encoding='utf-8')
        csv_reader = csv.reader(f)
        next(csv_reader)  # 컬럼데이터를 빼주기 위해 한번 실행
        for row in csv_reader:
            values = ''
            for i in row:
                values += i + ','

            query = "INSERT INTO \"" + self.__super_name + "\" VALUES(" + values.rstrip(',') + ")"
            self.__cur.execute(query)

        f.close()
        self.__db.commit()
