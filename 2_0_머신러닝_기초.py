import pandas as pd
from sklearn.svm import SVC #pip install sklearn
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


df = pd.read_csv("./iris.csv")
y = df["variety"]
x = df[["sepal.length", "sepal.width", "petal.length", "petal.width"]]
train_x, test_x, train_y, test_y = train_test_split(x, y)

model = SVC() #Support Vector Machine Classifier
model.fit(train_x, train_y) #학습

result = model.predict(test_x)
score = accuracy_score(result, test_y) #채점
print(score)