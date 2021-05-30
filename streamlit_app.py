import streamlit as st
from PIL import Image
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import load_model
import numpy as np

st.title('5조 Dear My Body :sunglasses:')
st.header('나만의 맞춤형 AI 건강관리 통합 서비스')

with st.beta_expander("서비스 소개 더보기"):
    st.write("""

  ㅇ 건강에 대한 관심은 예전부터 매우 높았으며, 이와 관련한 서비스 니즈는 계속 증가할 것임
     - 과거에는 건강과 관련된 활동들이 하나의 ‘트렌드’ 로 인식되어 왔음 (‘00년대 웰빙, ‘10년대 힐링)
      → 경제성장, 개인 인식 변화 등으로 건강에 대한 관심은 더 이상 트렌드가 아닌 당연한 것으로 인식됨

  ㅇ 건강/운동에 대한 다양한 서비스가 파편화 되어 존재하고 있음
    - 나이키 러닝 클럽(NRC), 눔, 채식한끼, 맛있저염 등

  ㅇ 파편화된 서비스들을 하나의 통합된 서비스로 제공 : 식단관리 - 운동관리 - 보조식품/영양제 쇼핑 통합
    - 음식 관련 정보 제공으로 편리하고 효율적인 식단 관리, 최적 음식 추천
    - 웨어러블 기계 연동하여 종합적인 건강상태 및 운동 정보 제공
    - 운동/건강과 관련된 쇼핑몰 연계

     """)
# st.subheader('바쁜 그대여 Dear My Body의 AI 통합 서비스로 똑똑하게 건강 챙기세요')
st.text('CNN 활용 한식 이미지 인식')
st.text('- 학습 데이터셋 : 한식 150종 X 1,000장 = 150,000장')


location = st.multiselect("선호하는 운동을 선택하세요. 나만의 AI 맞춤 서비스 제공에 활용됩니다.",
                          ("헬스", "라이딩", "등산",
                           "클라이밍", "배드민턴", "수영"))
st.write(len(location), "가지를 선택했습니다.")


img = Image.open("./Img_test_chicken.jpg")
st.image(img, width=400, caption="입력 데이터 : 후라이드치킨")

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