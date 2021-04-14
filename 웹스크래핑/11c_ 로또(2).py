from bs4 import BeautifulSoup
import urllib.request as req
import urllib.parse as par
import matplotlib.pyplot as plt

lotto = [0 for i in range(45)]
num = 0
f = open("Lotto.txt", "a")
while True:
    num += 1
    query = par.quote("로또" + str(num) + "회")
    url = "https://search.naver.com/search.naver?sm=top_hty&fbm=0&ie=utf8&query={}".format(query)
    code = req.urlopen(url)

    soup = BeautifulSoup(code, 'html.parser')
    number = soup.select("#_lotto > div.lotto_wrap > div.num_box > span")

    if len(number) == 0:
        break
    # if num == 9:
    #     break

    print("{} 회 : ".format(num), end="")
    f.write("{} 회 : ".format(num))
    for i in number:
        if i.string == "보너스번호":
            print("+", end=" ")
            continue
        print(i.string, end=" ")
        f.write(i.string + " ")
        lotto[int(i.string) - 1] += 1  # 로또번호 각각의 출현 빈도수 카운트
    print()
    f.write("\n")


x = range(1, 46)  # x축 데이터
plt.bar(x, lotto, tick_label=x)
plt.show()
