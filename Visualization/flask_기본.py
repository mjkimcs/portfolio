# pip install flask

from flask import Flask, render_template # flask는 개발자가 모듈에 맞춰야하므로 엄밀히 말하면 모듈이 아닌 프레임워크

# 내 컴퓨터를 서버로 만들기
app = Flask(__name__)

@app.route("/") # 여기에 /test라고 쓰면 url주소는 0.0.0.0/test 라고 써줘야 함
def main():
    return render_template("index.html") # 서버가 클라이언트에게 던져주는 값

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)

# 오류 발생 시,
# host="172.30.1.52" 이라고 내 ip를 넣거나
# host="0.0.0.0" 이라고 해놓고, 에러가 발생한 주소창에 "127.0.0.1" 라고 하거나 "내 ip" 넣기
# 127.0.0.1 : 로컬 ip 주소, 어떤 PC든 그 PC의 ip 주소를 표현

# 명령 프롬프트 - ipconfig - IPv4 주소가 내 ip
# 내 ip : 172.30.1.52

# bootstrap template - Templates - Admin&Dashboard - Free Download
# 파이참 - New Directory 2개 생성 (이름은 static과 templates)
# 다운받은 파일들을 static에 저장
# static - dist 에 있는 index.html은 templates에 저장
# index.html 파일을 열어서 href와 src를 찾으면서 파일경로 수정하기 ../static/dist/
