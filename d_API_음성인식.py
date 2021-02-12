# https://www.ncloud.com/
# 서비스 - AI Service - CSS
# 이용 신청하기
# 로그인 - 콘솔 - Products & Services
# AI NAVER API
# Application 등록 - 이름 test - https://test.com - 등록
# 인증정보 ID와 Secret

import sys
import requests

api_id = "m8ilvwptqm"
api_pw = "ZiqnuNGTdE2hARjeqzOJt1liDVvO0PI6gm0zaKwm"

client_id = api_id
client_secret = api_pw
lang = "Kor"
url = "https://naveropenapi.apigw.ntruss.com/recog/v1/stt?lang=" + lang
data = open('./음성파일예시.mp3', 'rb')
headers = {
    "X-NCP-APIGW-API-KEY-ID": client_id,
    "X-NCP-APIGW-API-KEY": client_secret,
    "Content-Type": "application/octet-stream"
}
response = requests.post(url,  data=data, headers=headers)
rescode = response.status_code
if(rescode == 200):
    print (response.text)
else:
    print("Error : " + response.text)