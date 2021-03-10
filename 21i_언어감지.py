#지도학습 활용: 모르는 것을 예측할 때, 어떤 것들의 연관성을 증명할 때
#본 실습은 언어 종류와 알파벳 출현 빈도수 간의 연관성을 증명한 것

import glob
import os
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.svm import SVC #분류모델 사용
from sklearn.metrics import accuracy_score #채점


def normalize_list(original_list):
    total_cnt = sum(original_list)
    list = []
    for i in original_list:
        list.append(i/total_cnt)
    return list

def frequency_alphabet(text): #각 알파벳의 출현 빈도
    text = text.lower()  #소문자로 변환
    code_a = ord("a") #ord: 문자의 아스키코드(숫자)를 반환
    code_z = ord("z")
    cnt_list = [0 for i in range(0, 26)]  #26개의 0
    for i in text:
        code_current = ord(i)
        if code_a <= code_current <= code_z:
            cnt_list[code_current - code_a] += 1
    return normalize_list(cnt_list)

def get_data_label(folder_name):
    files = glob.glob("./머신러닝/language/{}/*.txt".format(folder_name)) #폴더 내 모든 txt파일 추출
    x = []
    y = []
    for i in files:
        basename = os.path.basename(i) #파일명
        lang = basename.split("-")[0]

        with open(i, "r", encoding="utf-8") as f: #txt파일 내용 추출
            text = f.read()
        cnt_list = frequency_alphabet(text)

        x.append(cnt_list)
        y.append(lang)
    return x, y

def my_graph(x, y):
    graph_dict = {}
    for i in range(0, len(y)):
        column = y[i]
        value = normalize_list(x[i])
        if not column in graph_dict:
            graph_dict[column] = value

    index = [[chr(i) for i in range(97, 97 + 26)]] #ord("a")=97, chr(97)="a"

    df = pd.DataFrame(graph_dict, index=index)
    df.plot(kind='bar', subplots=True, ylim=(0, 0.15))
    plt.show()


train_x, train_y = get_data_label("train")
test_x, test_y = get_data_label("test")
my_graph(train_x, train_y)

model = SVC()
model.fit(train_x, train_y)
predict = model.predict(test_x) #test_x는 [[]]형
score = accuracy_score(predict, test_y)
print(score)

sentence = "Democracy (Greek: δημοκρατία, dēmokratiā, from dēmos 'people' and kratos 'rule') is a form of government in which the people have the authority to choose their governing legislators. The decisions on who is considered part of the people and how authority is shared among or delegated by the people have changed over time and at different speeds in different countries, but they have included more and more of the inhabitants of all countries. Cornerstones include freedom of assembly and speech, inclusiveness and equality, membership, consent, voting, right to life and minority rights."
test_sentence = frequency_alphabet(sentence)
predict = model.predict([test_sentence]) #원래 [[]]이지만, test_sentence가 []형이므로 한 묶음만 더 써줌
print(predict)