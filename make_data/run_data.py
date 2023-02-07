import streamlit as st

from transformers import AutoTokenizer

@st.cache()
def setting():
    tokenizer = AutoTokenizer.from_pretrained(
        'kakaobrain/kogpt', revision='KoGPT6B-ryan1.5b-float16',  # or float32 version: revision=KoGPT6B-ryan1.5b
        bos_token='[BOS]', eos_token='[EOS]', unk_token='[UNK]', pad_token='[PAD]', mask_token='[MASK]'
        )
    return tokenizer

tokenizer = setting()
    
def decomposition(paragraph):
    sentences = paragraph.split('.')
    output_list = []
    for sent in sentences:
        input_idx = tokenizer.encode(sent)
        output = []
        for i in input_idx:
            out = tokenizer.decode(i)
            output.append(out)
        output_list.append[output]
    return output_list


st.title('데이터 생성기')

tab1, tab2 = st.tabs(['데이터 생성', '데이터 확인'])

with tab1:
    sentence_list = st.text_area(label='문장 입력', value='')
    
    if st.button('분해'):
        for sentence in sentence_list:
            st.write(decomposition(sentence))
    
with tab2:
    st.title('데이터 확인')