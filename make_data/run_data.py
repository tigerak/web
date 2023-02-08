import pandas as pd
import streamlit as st

from transformers import AutoTokenizer


tokenizer = AutoTokenizer.from_pretrained(
    'kakaobrain/kogpt', revision='KoGPT6B-ryan1.5b-float16',  # or float32 version: revision=KoGPT6B-ryan1.5b
    bos_token='[BOS]', eos_token='[EOS]', unk_token='[UNK]', pad_token='[PAD]', mask_token='[MASK]'
    )
    
def decomposition(paragraph):
    sentences = paragraph.split('.')
    output_list = []
    for sent in sentences:
        input_idx = tokenizer.encode(sent)
        output = []
        for i in input_idx:
            out = tokenizer.decode(i)
            output.append(out)
        output_list.append(output)
    return output_list

# def render_selectors(ui_spec, n_col):
#     field_cols = st.columns([1]*n_col)
#     for i, spec in enumerate(ui_spec):
#         selector = spec['selector']
#         with field_cols[i%n_col]:
#             selector['type'](selector['label'], key=selector['key'], **selector['kwargs'])
            
def get_selector_values(ui_spec):
    values = {}
    for spec in ui_spec:
        selector = spec['selector']
        values[selector['key']] = {
            'label': selector['label'], 
            'value': st.session_state[selector['key']],
        }
    return values


st.title('데이터 생성기')

tab1, tab2 = st.tabs(['데이터 생성', '데이터 확인'])

with tab1:
    # 1. Create a variable to store todos.
    if not 'wordlist' in st.session_state:
        st.session_state.wordlist = []
    
    # Prompt the user in the form
    with st.form(key='paragraph'):
        paragraph = st.text_area(label='문단 입력', value='')
        is_submit = st.form_submit_button('분해 시작')
        
    # 3. Store todo in todolist when submit button is hit.
    if is_submit:
        sentence_list = decomposition(paragraph)
        st.session_state.wordlist = sentence_list
        
    # 4. Display the contents of todolist
    n_col = 6
    for i, sentence in enumerate(st.session_state.wordlist):
        # with st.expander(label='List of words', expanded=True):
        with st.form(key=f'{i}'):
            field_cols = st.columns([1]*n_col)
            for j, word in enumerate(sentence):
                with field_cols[j%n_col]:
                    st.checkbox(label=f'{word}', key=f'{i}_{j}')
            if st.form_submit_button('선택 완료'):
                st.write([k for k, v in st.session_state.items() if v == True])


                
                
    # if st.button('분해'):
    #     sentence_list = decomposition(paragraph)
        
    #     # 컨테이너 설정
    #     # container = st.container()
    #     # column 개수 설정
    #     c = 6
    #     for i, sentence in enumerate(sentence_list):
    #         # df = pd.DataFrame(columns=range(c))
    #         # d = {}
    #         with st.expander(f"See explanation {i+1} sentence"):
    #             UI_SPECIFICATION = []
    #             for j, word in enumerate(sentence):
                    
    #             #     if (i%c == c-1) or (i+1 == len(sentence)):
    #             #         d[i%c] = word
    #             #         df.loc[i//c] = d
    #             #         d = {}
    #             #     else:
    #             #         d[i%c] = word
                        
    #                 form = {
    #                     'selector': {
    #                         'key': str(i) + '_' + str(j),
    #                         'type': st.checkbox,
    #                         'label': word,
    #                         'kwargs': {'value': False, 'disabled': False},
    #                         }
    #                 }

    #                 UI_SPECIFICATION.append(form)
                    
    #             render_selectors(UI_SPECIFICATION, c)
    #             st.button('선택 완료', key=i)
    # for k in st.session_state.keys():
    #     st.write(k)
                # selector_values = get_selector_values(UI_SPECIFICATION)

                # st.dataframe(df, use_container_width=True)
            
    
with tab2:
    st.subheader('데이터 확인')
    # # 1. Create a variable to store todos.
    # if not 'wordlist' in st.session_state:
    #     st.session_state.wordlist = []
        
    # # 2. Prompt the user in the form
    # with st.form(key='form'):
    #     paragraph = st.text_area(label='문단 입력', value='')
    #     is_submit = st.form_submit_button('분해 시작')
        
    # # 3. Store todo in todolist when submit button is hit.
    # if is_submit:
    #     sentence_list = decomposition(paragraph)
    #     st.session_state.wordlist = []
    #     for i, sentence in enumerate(sentence_list):
    #         for j, word in enumerate(sentence):
    #             st.session_state.wordlist.append(word)
        
    # # 4. Display the contents of todolist
    # n_col = 6
    # with st.expander(label='List of words', expanded=True):
    #     field_cols = st.columns([1]*n_col)
    #     for i, todo_text in enumerate(st.session_state.wordlist):
    #         with field_cols[i%n_col]:
    #             st.checkbox(label=f'{todo_text}', key=f'{i}')


    
        
    