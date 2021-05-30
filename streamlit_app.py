import streamlit as st
from PIL import Image
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import load_model
import numpy as np

st.title('5조 Dear My Body')
st.header('나만의 맞춤형 AI 건강관리 통합 서비스')
# st.subheader('바쁜 그대여 Dear My Body의 AI 통합 서비스로 똑똑하게 건강 챙기세요')
st.text('CNN 활용 한식 이미지 인식')
st.text('- 학습 데이터셋 : 한식 150종 X 1,000장 = 150,000장')


location = st.multiselect("선호하는 운동을 선택하세요. 나만의 AI 맞춤 서비스 제공에 활용됩니다.",
                          ("헬스", "라이딩", "등산",
                           "클라이밍", "배드민턴", "수영"))
st.write(len(location), "가지를 선택했습니다.")


img = Image.open("./Img_test_chicken.jpg")
st.image(img, width=400, caption="입력 데이터 : 꿀떡")

if st.button("분석하기"):
    path = "./Img_test_chicken.jpg"
    img = keras.preprocessing.image.load_img(
     path, target_size=(180, 180)
    )

    img_array = keras.preprocessing.image.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)  # Create a batch
    model = keras.models.load_model('./kf_model.h5')
    predictions = model.predict(img_array)
    score = tf.nn.softmax(predictions[0])
    class_names = ['불고기', '전복죽', '후라이드치킨']

    st.text(
     "예측값: {}(정확도 {:.2f}%)"
         .format(class_names[np.argmax(score)], 100 * np.max(score))
    )


message = st.text_area("불편사항을 알려주세요.")
if st.button("Submit"):
    if message.title():
        st.success("귀하의 소중한 의견은 서비스 개선에 적극 반영하겠습니다. 감사합니다.")
    else:
        st.error("텍스트를 입력해주세요")

# streamlit run streamlit_app.py