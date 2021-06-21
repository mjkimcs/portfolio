import cx_Oracle
from tkinter import messagebox
from konlpy.tag import Okt
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model
import json
from pymongo import MongoClient
import os
from bson.json_util import dumps

class OracleToMongoDB:
    def __init__(self):
        __client = MongoClient()
        __mydb = __client["naver_movie"]
        self.__mycol = __mydb["project"]

    def Morpheme(self, super_name):
        self.__mycol.drop()

        __dsn = cx_Oracle.makedsn("localhost", 1521, 'xe')
        __db = cx_Oracle.connect('SCOTT', 'TIGER', __dsn)
        __cur = __db.cursor()

        self.__okt = Okt()  # 형태소 분석기
        self.__tokenizer = Tokenizer(19417, oov_token='OOV')
        with open('Supports/wordIndex.json') as json_file:  # {'영화':4, '좋다':7, ...}
            word_index = json.load(json_file)
            self.__tokenizer.word_index = word_index

        self.__loaded_model = load_model('Supports/best_model.h5')  # 미리 훈련시킨 딥러닝 모델

        __cur.execute("SELECT * FROM \"" + super_name + "\"")
        __db_data = __cur.fetchmany(500)
        for row in __db_data:
            if row[1] is not None:
                score = self.__sentiment_predict(row[1])
                if score >= 0.5:
                    self.__mycol.insert_one({"rate": row[0], "note": row[1], "date": row[2],
                                             "good": row[3], "bad": row[4], "sympathy": '긍정'})
                else:
                    self.__mycol.insert_one({"rate": row[0], "note": row[1], "date": row[2],
                                             "good": row[3], "bad": row[4], "sympathy": '부정'})

        messagebox.showinfo("완료", "긍부정 형태소분석이 완료되었습니다.")

        __cur.close()
        __db.close()

        self.refined_data_write(super_name)

        return True

    def refined_data_write(self, super_name):
        folder_path = "Refined_data"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        path = folder_path + "/" + super_name + ".json"
        if os.path.exists(path):
            if os.path.exists(path):
                os.remove(path)

        f = open(path, "w", encoding='utf-8')

        cursor = self.__mycol.find()

        list_cur = list(cursor)

        json_data = dumps(list_cur, indent=2)
        f.write(json_data)

        f.close()

    def __sentiment_predict(self, new_sentence):
        # print(new_sentence)
        max_len = 30
        stopwords = ['의', '가', '이', '은', '들', '는', '좀', '잘', '걍', '과', '도', '를', '으로', '자', '에', '와', '한', '하다', '##',
                     '입력']
        new_sentence = self.__okt.morphs(new_sentence, stem=True)  # 토큰화
        new_sentence = [word for word in new_sentence if not word in stopwords]
        encoded = self.__tokenizer.texts_to_sequences([new_sentence])  # 빈도수에 따라 정수 인코딩
        pad_new = pad_sequences(encoded, maxlen=max_len)  # 패딩
        score = float(self.__loaded_model.predict(pad_new))  # 예측
        return score

    def normal(self):
        table = self.__mycol.find({}, {"_id": 0})

        hi = []
        for i in table:
            hi2 = []
            for j in i.values():
                hi2.append(j)
            hi.append(hi2)

        return hi

    def star(self):
        table1 = self.__mycol.aggregate(
            [{"$group": {
                "_id": '$rate',
                "게시글수": {"$sum": 1},
                "좋아요수": {"$sum": "$good"},
                "싫어요수": {"$sum": "$bad"},
                "긍정수": {"$sum": {"$cond": {"if": {"$eq": ["$sympathy", "긍정"]}, "then": 1, "else": 0}}}
            }},
                {"$addFields": {"부정수": {"$subtract": ["$게시글수", "$긍정수"]}}},
                {"$addFields": {"긍정비율": {"$divide": [{"$multiply": ["$긍정수", 100]}, "$게시글수"]}}},
                {"$addFields": {"부정비율": {"$divide": [{"$multiply": ["$부정수", 100]}, "$게시글수"]}}},
                {"$project": {"게시글수": 1, "좋아요수": 1, "싫어요수": 1, "긍정수": 1, "부정수": 1,
                              "긍정비율": {"$concat": [{"$toString": {"$round": ["$긍정비율", 2]}}, "%"]},
                              "부정비율": {"$concat": [{"$toString": {"$round": ["$부정비율", 2]}}, "%"]}
                              }
                 },
                {"$sort": {"_id": 1}}
            ])

        hi = []
        for i in table1:
            hi2 = []
            for j in i.values():
                hi2.append(j)
            hi.append(hi2)

        return hi

    def date(self):
        table2 = self.__mycol.aggregate(
            [{"$group": {
                "_id": '$date',
                "게시글수": {"$sum": 1},
                "좋아요수": {"$sum": "$good"},
                "싫어요수": {"$sum": "$bad"},
                "별점평균": {"$avg": "$rate"},
                "긍정수": {"$sum": {"$cond": {"if": {"$eq": ["$sympathy", "긍정"]}, "then": 1, "else": 0}}}
            }},
                {"$addFields": {"부정수": {"$subtract": ["$게시글수", "$긍정수"]}}},
                {"$addFields": {"긍정비율": {"$divide": [{"$multiply": ["$긍정수", 100]}, "$게시글수"]}}},
                {"$addFields": {"부정비율": {"$divide": [{"$multiply": ["$부정수", 100]}, "$게시글수"]}}},
                {"$project": {"게시글수": 1, "좋아요수": 1, "싫어요수": 1, "긍정수": 1, "부정수": 1,
                              "긍정비율": {"$concat": [{"$toString": {"$round": ["$긍정비율", 2]}}, "%"]},
                              "부정비율": {"$concat": [{"$toString": {"$round": ["$부정비율", 2]}}, "%"]},
                              "별점평균": {"$round": ["$별점평균", 2]}}},
                {"$sort": {"_id": 1}}
            ])

        hi = []
        for i in table2:
            hi2 = []
            for j in i.values():
                hi2.append(j)
            hi.append(hi2)

        return hi

    def sympathy(self):
        table3 = self.__mycol.aggregate(
            [{"$group": {
                "_id": '$sympathy',
                "별점평균": {"$avg": "$rate"},
                "게시글수": {"$sum": 1},
                "좋아요수": {"$sum": "$good"},
                "싫어요수": {"$sum": "$bad"}
            }},
                {"$project": {"게시글수": 1, "좋아요수": 1, "싫어요수": 1, "별점평균": {"$round": ["$별점평균", 2]}
                              }},
                {"$sort": {"_id": 1}}
            ])

        hi = []
        for i in table3:
            hi2 = []
            for j in i.values():
                hi2.append(j)
            hi.append(hi2)

        return hi
