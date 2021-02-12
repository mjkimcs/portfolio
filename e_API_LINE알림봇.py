#line notify api
#앱 - 더보기 - 톱니바퀴 - 계정
#웹 - 마이페이지 - Generate token
#LINE Notify API Cocument - Notification

import requests

api_key = "I8Fuv6Ua5vBBAtnV01qOqsijkwfdce4GQeQNFjt9HCX"
headers = {"Authorization" : "Bearer {}".format(api_key)}
data = {"message" :"테스트 톡"}
requests.post("https://notify-api.line.me/api/notify", headers=headers, data=data)

#단톡방 만들기

api_key = "v5yeBTdhOkj3CmJVKfGVTCmybLT2IXlAauv3wfjHJVh"
headers = {"Authorization" : "Bearer {}".format(api_key)}
data = {"message" :"테스트 단톡"}
requests.post("https://notify-api.line.me/api/notify", headers=headers, data=data)
