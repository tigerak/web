import streamlit as st

from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained(
    'kakaobrain/kogpt', revision='KoGPT6B-ryan1.5b-float16',  # or float32 version: revision=KoGPT6B-ryan1.5b
    bos_token='[BOS]', eos_token='[EOS]', unk_token='[UNK]', pad_token='[PAD]', mask_token='[MASK]'
    )

@st.cache()
def decomposition(sentence):
    input_idx = tokenizer.encode(sentence)
    output = []
    for i in input_idx:
        out = tokenizer.decode(i)
        output.append(out)
    return output


st.title('데이터 생성기')

tab1, tab2 = st.tabs(['데이터 생성', '데이터 확인'])

with tab1:
    sent = st.text_area(label='문장 입력', value='')
    
    if st.button('분해'):
        st.write(decomposition(sent))
    
with tab2:
    st.title('데이터 확인')