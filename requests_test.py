import requests
url = "https://google.com"
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36"}
res = requests.get(url, headers=headers)
# print("응답코드 :", res.status_code) # 정상은 200, 비정상은 403
res.raise_for_status() # 문제가 있으면 오류를 내뱉고 프로그램 종료

with open("mygoogle.html", "w", encoding="utf8") as f:
    f.write(res.text)
