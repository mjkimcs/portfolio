#네이버 메일함 - 하단에 환경설정 - POP3/IMAP 설정 - 사용함 - 원본저장 - 확인
#SMTP 서버명, 포트, SSL필요여부 확인

import openpyxl
from email.mime.text import MIMEText
import smtplib
from email.mime.base import MIMEBase #첨부파일 전송 시 필요
from email.mime.multipart import MIMEMultipart #첨부파일 전송 시 필요
from email import encoders #첨부파일 전송 시 필요

#메일 서버 로그인
naver_server = smtplib.SMTP_SSL("smtp.naver.com", 465) #SSL필요, 서버명, 포트
naver_server.login("11lalala", "1234")

book = openpyxl.load_workbook("./list.xlsx")
sheet = book.active
cnt = 0 #한꺼번에 많이 보내면 차단 당하므로 미연에 방지
for row in sheet.rows: #각 행을 가져옴
    if row[4].value == "X": #row[4] : 가져온 행의 4번째 셀
        continue
    date = row[0].value
    name = row[1].value
    address = row[2].value
    product = row[3].value
    title = "{}님, 민정 쇼핑몰입니다.".format(name)
    content = """
안녕하세요. 민정 쇼핑몰입니다.
결제 완료 안내 메일입니다.

성함 : {}
날짜 : {}
상품 : {}""".format(name, date, product)

    msg = MIMEMultipart() #첨부파일도 넣기위한 큰 편지봉투
    msg["From"] = "11lalala@naver.com"
    msg["To"] = "address"
    # msg["Cc"] = "od3366@naver.com, mjkimcs@kaist.ac.kr"
    msg["Subject"]= title
    # msg = MIMEText(content, _charset="euc-kr") #첨부파일 없는 편지봉투
    # msg["From"] = "11lalala@naver.com"
    # msg["To"] = address
    # msg["Subject"] = title

    msg_r = MIMEText(content, _charset="euc-kr")
    msg.attach(msg_r)

    part = MIMEBase("application", "octet-stream") #excel,word파일 첨부
    # MIMEBase("image", "jpg") #이미지파일 첨부
    part.set_payload(open("./attachment_file.xlsx", "rb").read()) #rb: 바이너리 형식
    encoders.encode_base64(part) #압축
    part.add_header("Content-Disposition", "attachment; filename=attachment_file.xlsx")
    msg.attach(part)

    naver_server.sendmail("11lalala@naver.com", address, msg.as_string()) #메일전송
    print("{}님께 메일전송 성공".format(name))

    cnt += 1 #한꺼번에 많이 보내면 차단 당하므로 미연에 방지
    if cnt % 20 == 0:
        naver_server.quit() #로그아웃 후 바로 다시 로그인
        naver_server = smtplib.SMTP_SSL("smtp.naver.com", 465)  # SSL필요, 서버명, 포트
        naver_server.login("11lalala", "1234")
