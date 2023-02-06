import streamlit as st

from util.sentence_decomp import decomposition

st.title('데이터 생성기')

tab1, tab2 = st.tabs(['데이터 생성', '데이터 확인'])

with tab1:
    sent = st.text_area(label='문장 입력', value='한 문장을 입력하세요')
    
    if st.button('분해'):
        st.write(decomposition(sent))
    
with tab2:
    st.title('데이터 확인')