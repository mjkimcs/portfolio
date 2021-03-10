# pip install flask
# pip install jpype1 bs4 tensorflow konlpy pyecharts==0.5.10 pyecharts_snapshot
# 오류 발생 시 pip install jpype1==1.2.0


from flask import Flask, render_template # pip install flask
from konlpy.tag import Okt
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model
import json
import os
from bs4 import BeautifulSoup
import urllib.request as req
from pyecharts import Bar3D # pip install pyecharts==0.5.10
from pyecharts import Pie

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

app = Flask(__name__)

okt = Okt()
tokenizer = Tokenizer(19417, oov_token = 'OOV')
with open('./wordIndex.json') as json_file:
  word_index = json.load(json_file)
  tokenizer.word_index = word_index

loaded_model = load_model('./best_model.h5')
def sentiment_predict(new_sentence):
    print(new_sentence) # 영화리뷰 문장
    max_len = 30
    stopwords = ['의','가','이','은','들','는','좀','잘','걍','과','도','를','으로','자','에','와','한','하다'] # 불용어
    new_sentence = okt.morphs(new_sentence, stem=True) # 토큰화
    new_sentence = [word for word in new_sentence if not word in stopwords] # 불용어 제거
    encoded = tokenizer.texts_to_sequences([new_sentence]) # 정수 인코딩
    pad_new = pad_sequences(encoded, maxlen = max_len) # 패딩
    score = float(loaded_model.predict(pad_new)) # 예측
    if 0.8 <= score <= 1.0:
      return "매우긍정"
    elif 0.6 <= score < 0.8:
      return "긍정"
    elif 0.4 <= score < 0.6:
      return "보통"
    elif 0.2 <= score <0.4:
      return "부정"
    else:
      return "매우부정"


page_num = 1
previous_page_result = ""
result_dic = {"매우긍정":0, "긍정":0, "보통":0, "부정":0, "매우부정":0}
while True:
    code = req.urlopen("https://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn?code=10106&type=after&isActualPointWriteExecute=false&isMileageSubscriptionAlready=false&isMileageSubscriptionReject=false&page={}".format(page_num))
    soup = BeautifulSoup(code, "html.parser")
    comment = soup.select("li > div.score_reple > p > span")
    if comment[-1].text.strip() == previous_page_result:
        break
    for i in comment:
        i = i.text.strip()
        if i == "관람객":
            continue
        result = sentiment_predict(i) # 매우긍정, 긍정, 보통, 부정, 매우부정 중 하나의 문자열로 반환
        # if score >= 0.5:
        #     print("{:.2f}% 확률로 긍정".format(score*100)) # :.2f 소수점 아래 2자리까지만
        # else:
        #     print("{:.2f}% 확률로 부정".format((1-score) * 100))
        result_dic[result] += 1
        print("---------------------------")
    previous_page_result = i
    page_num += 1
    if page_num == 2:
        break


# 감성분석 시각화 - 3차원막대

bar3d = Bar3D("감성분석 결과", width=600, height=300)
x_axis = ["매우긍정", "긍정", "보통", "부정", "매우부정"]
y_axis = []
data = [[0, 0, result_dic["매우긍정"]], [0, 1, result_dic["긍정"]], [0, 2, result_dic["보통"]], [0, 3, result_dic["부정"]], [0, 4, result_dic["매우부정"]]]
range_color = ['#313695', '#4575b4', '#74add1', '#abd9e9', '#e0f3f8', '#ffffbf',
               '#fee090', '#fdae61', '#f46d43', '#d73027', '#a50026']
bar3d.add("", x_axis, y_axis, [[d[1], d[0], d[2]] for d in data],
    is_visualmap=True, visual_range=[0, 170], visual_range_color=range_color,
    grid3d_width=200, grid3d_depth=40)
bar3d.render("./bar3d.html") # 원하는 파일명 지정


# 감성분석 시각화 - 파이

attr = ["매우긍정", "긍정", "보통", "부정", "매우부정"]
v1 = [result_dic["매우긍정"],result_dic["긍정"],result_dic["보통"],result_dic["부정"],result_dic["매우부정"]]
pie = Pie("감정분석 결과")
pie.add("", attr, v1, is_label_show=True)
pie.render("./pie.html")


total = sum(result_dic.values()) # values함수는 딕셔너리형에 있는 값만 추출
emotion1 = result_dic["매우긍정"] / total
emotion2 = result_dic["긍정"] / total
emotion3 = result_dic["부정"] / total
emotion4 = result_dic["매우부정"] / total


f = open("./bar3d.html", "r", encoding="utf-8") # UnicodeDecodeError 에러 발생 시 encoding="utf-8" 옵션 넣어주기
bar3d_code = f.read()
f.close()
f = open("./pie.html", "r", encoding="utf-8")
pie_code = f.read()
f.close()


@app.route("/") # 여기에 /test라고 쓰면 url주소는 0.0.0.0/test 라고 써줘야 함
def main():
    return render_template("index.html", e1="매우긍정 : {:.2f}%".format(emotion1*100), e2="긍정 : {:.2f}%".format(emotion2*100), e3="부정 : {:.2f}%".format(emotion3*100), e4="매우부정 : {:.2f}%".format(emotion4*100),
                           bar3d=bar3d_code, pie=pie_code) # 서버가 클라이언트에게 던져주는 값
# index.html 파일 수정 시
# {{e1}} 이렇게 중괄호 2개 써줌
# 예를들어 <div class="card-body"><canvas id="myBarChart" width="100%" height="40"></canvas></div> 를
# <div class="card-body">{{pie}}</canvas></div> 이렇게 수정
# 끝난 게 아님!
# pie.html 코드가 시각화되려면 |safe 넣어줘야 함 <div class="card-body">{{pie|safe}}</canvas></div> 이렇게 수정

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80) # 에러가 발생한 주소창에 "127.0.0.1" 라고 하거나 "내 ip" 넣기


# AWS ec2 - 서비스 - EC2 - 인스턴스 시작 - 검색창에 windows 검색 - 프리티어 사용가능 클릭
# - 프리티어 사용가능 체크 - 검토 및 시작 - 시작하기 - 새 키 페어 생성 - 이름 flask-test
# - 키 페어 다운로드 - 저장 - ~.pem 파일 - 인스턴스 시작
# - 예상요금 알림받기 설정- 결제 알림 생성 - 모두 체크 - 기본설정저장
# - 인스턴스 보기 - 가로로 스크롤 넘겨서 보안 그룹 이름 확인
# - 왼쪽 메뉴 보안그룹 탭 클릭 - 보안그룹 ID 클릭 - 인바운드 규칙 - 인바운드 규칙 편집
# - 규칙 추가 - 시용자 지정 TCP 포트범위 5000 - 0.0.0.0/0
# - 규칙 추가 - 모든 TCP - 위치무관 - 규칙저장
# - 왼쪽 메뉴 인스턴스 탭 클릭 - 인스턴스 ID 우클릭 - 연결 - RDP클라이언트 - Public DNS와 사용자이름 복사해두기 - 암호가져오기 - 키 페어로 이동 - 암호해독 - 비밀번호 복사
# - PC 검색탭 Microsoft Store - microsoft remote desktop 다운받기 - Add a PC
# - PC name에 Public DNS 넣기 - Add a User Account에 사용자 이름과 암호 넣기 - Add - Add - 더블클릭

# 내PC에서 파이썬 설치파일 복사한 후 원격화면에 붙여넣기
# 내PC에서 jdk 구글링 - Java Development Kit - Windows x64 다운로드 - jdk 설치파일도 원격화면에 붙여넣기
# 원격화면 - 탐색기 - This PC - 우클릭 Properties - Advanced system settings - Environment Variables - System Variables - New - Name: JAVA_HOME - Browse Directory - This PC - C - Program Files - Java - jdk - ok
# 원격화면 - cmd 검색 - pip install flask jpype1 bs4 konlpy tensorflow pyecharts==0.5.10 pyecharts_snapshot
# 원격화면 - 새폴더 생성 - 폴더명 server
# - 내PC에서 best_model.h5 wordIndex.json bar3d.html pie.html 3_3_flask_웹페이지.py static templates 복사한 후 원격화면 새폴더에 붙여넣기
# - 3_3_flask_웹페이지.py을 main.py로 파일명 변경 - 우클릭 - Edit with IDLE - 파일의 전체경로 써주기(r'C:\Users\Administrator\Desktop\server\wordIndex.json')
# - f = open("./bar3d.html", "r", encoding="utf-8") 으로 수정
# - loaded_model에 , compile=False 옵션 추가하여 수정
# - port=5000 으로 수정 - File메뉴 - Save

# 외부와의 통신을 위해 방화벽 뚥어주기
# 원격화면 - 검색 탭 - firewall - Advanced Settings - Inbound Rules - New Rule - Port - Next - 5000 ports - Next - Allow the connection - Next - Next - Name: flask_server - Finish

# 원격화면 cmd - cd Desktop - cd server - python mail.py - 에러가 나면
# - 내PC에서 구글링 c++ redistributable - 재배포 가능 - 다운로드 - 64비트 - 저장 - 설치파일 복사 후 원격화면에 붙여넣기 - 설치 - 다시실행 - 에러가 나면
# - pip uninstall tensorflow - y - pip install tensorflow==1.15.0 - 다시실행

# 원격화면 꺼도 AWS 서버가 계속 돌아가게 설정
# 원격화면 - server폴더 - New - Text - flask_server라고 이름짓기 - 아래 명령어 넣기
# Set objShell = WScript.CreateObject("WScript.Shell")
# objShell.Run "cmd /c python C:\Users\Administrator\Desktop\server\main.py", 0
# server폴더 - View 메뉴 - File name extensions 체크 - flask_server.txt 우클릭 - Rename - .txt를 .vbs로 바꿔줌

# 내PC - Public DNS 복사 후 주소창에 붙여넣기 - 맨 앞에 http:// - 맨 뒤에 :5000

