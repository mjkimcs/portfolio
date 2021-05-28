import cx_Oracle

def Test01():
    dsn = cx_Oracle.makedsn("localhost", 1521, "xe")  # 오라클 주소
    conn = cx_Oracle.connect("SCOTT", "TIGER", dsn)  # 오라클 접속
    cursor = conn.cursor()
    cursor.execute("select empno, ename, sal, deptno from emp")
    row = cursor.fetchall()
    print(row)

def Test02():
    dsn = cx_Oracle.makedsn("localhost", 1521, "xe")  # 오라클 주소
    conn = cx_Oracle.connect("SCOTT", "TIGER", dsn)  # 오라클 접속
    cursor = conn.cursor()
    cursor.execute("""select e.ename, e.deptno, d.loc 
    from emp e, dept d 
    where E.DEPTNO = D.DEPTNO and e.sal >= 2500""")
    row = cursor.fetchall()
    print(row)

def Test03():
    dsn = cx_Oracle.makedsn("localhost", 1521, "xe")  # 오라클 주소
    conn = cx_Oracle.connect("SCOTT", "TIGER", dsn)  # 오라클 접속
    cursor = conn.cursor()
    cursor.execute("""select ename, deptno, loc 
    from emp join dept using(deptno) 
    where sal >= 2500""")
    row = cursor.fetchall()
    print(row)

if __name__ == '__main__':
    Test01()
    print("======================")
    Test02()
    print("======================")
    Test03()