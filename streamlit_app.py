import streamlit as st

st.title('5조 Dear My Body 한식 이미지 인식')
st.header('CNN 활용 이미지 인식')
st.subheader('학습 데이터셋 : 한식 150종 X 1,000장 = 150,000장')


if st.button("분석하기"):
 st.text(" 확률로 이미지 입니다")


message = st.text_area("불편사항을 알려주세요.")
if st.button("Submit"):
    if message.title():
        st.success("귀하의 소중한 의견은 서비스 개선에 적극 반영하겠습니다. 감사합니다.")
    else:
        st.error("텍스트를 입력해주세요")

# streamlit run streamlit.py