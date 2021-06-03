# 파이참 - file - settings - python interpreter - cx-Oraclet설치
# https://cx-oracle.readthedocs.io/en/latest/user_guide/connection_handling.html
# https://cx-oracle.readthedocs.io/en/latest/user_guide/sql_execution.html
# cmd - sqlplus SCOTT/TIGER@localhost:1521/xe

import cx_Oracle

def myCon():
    dsn = cx_Oracle.makedsn("localhost", 1521, service_name="XE")  # 오라클 주소
    conn = cx_Oracle.connect(user="SCOTT", password="TIGER", dsn=dsn, encoding="UTF-8")  # 오라클 접속
    print(conn)
    return conn

def Test01(conn):
    cur = conn.cursor()  # 실행결과 데이터를 담을 메모리 객체
    for i in cur.execute("select * from EMP"):
        print(i)

def Test02(conn):
    cur = conn.cursor()
    cur.execute("select * from EMP")
    while True:
        row = cur.fetchone()
        if row is None:
            break
        print(row)

def Test03(conn):
    cur = conn.cursor()
    cur.execute("select * from DEPT")
    num_rows = 10
    while True:
        rows = cur.fetchmany(num_rows)
        if not rows:
            break
        for row in rows:
            print(row)

def Test04(conn):
    cur = conn.cursor()
    cur.execute("select * from dept")
    rows = cur.fetchall()
    for row in rows:
        print(row[0], row[1])


if __name__ == '__main__':
    Test01(myCon())
    print("========================")
    Test02(myCon())
    print("========================")
    Test03(myCon())
    print("========================")
    Test04(myCon())
