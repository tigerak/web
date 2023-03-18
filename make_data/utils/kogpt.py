# from transformers import AutoTokenizer

# Load KOGPT Tokenizer
# tokenizer = AutoTokenizer.from_pretrained(
#     'kakaobrain/kogpt', revision='KoGPT6B-ryan1.5b-float16',  # or float32 version: revision=KoGPT6B-ryan1.5b
#     bos_token='[BOS]', eos_token='[EOS]', unk_token='[UNK]', pad_token='[PAD]', mask_token='[MASK]'
#     )

# Deconposition : paragraph -> token
# def decomposition(paragraph):
#     sentences = paragraph.split('.')
#     output_list = []
#     for s_k, sent in enumerate(sentences):
#         input_idx = tokenizer.encode(sent)
#         output = {}
#         for w_k, i in enumerate(input_idx):
#             out = tokenizer.decode(i)
#             make_key = str(s_k) + '_' + str(w_k) + '_' + out
#             output[make_key] = out
#         output_list.append(output)
#     return output_list

def decomposition(paragraph):
    sentences = paragraph.split('.')
    output_list = []
    for s_k, sent in enumerate(sentences):
        words = sent.split(' ')
        output = {}
        for w_k, word in enumerate(words):
            make_key = str(s_k) + '_' + str(w_k) #+ '_' + word
            output[make_key] = word
        output_list.append(output)
    return sentences, output_list

from make_data.models.database import User_only
from make_data.extensions import db
from flask import render_template, request, redirect
def sign(post_form):
        # Get User ID
        user_id = post_form['user_id']
        # User list
        user_list = {'등록된 ID 목록' : []}
        for i in User_only.query.with_entities(User_only.user_id).all():
            user_list['등록된 ID 목록'].append(i[0])
            
        # Sign in
        if post_form['choice'] == 'Sign in':
        
            if user_id == '':
                message = 'ID를 입력하지 않았습니다.'
                return render_template('index.html', message=message, user_list=user_list)
            
            elif user_id not in user_list['등록된 ID 목록']:
                message = '없는 ID 입니다.'
                return render_template('index.html', message=message, user_list=user_list)
            
            elif user_id in user_list['등록된 ID 목록']:
                return redirect(f'/api/{user_id}')
            
        # Sign UP
        elif request.form['choice'] == 'Sign up':
            
            if user_id not in user_list['등록된 ID 목록']:
                send_api_data = User_only(user_id, 'prompt', 'completion')
                db.session.add(send_api_data)
                db.session.commit()
                
                message = 'ID가 등록되었습니다. \nSign in 해주세요.'
                
                user_list = {'등록된 ID 목록' : []}
                for i in User_only.query.with_entities(User_only.user_id).all():
                    user_list['등록된 ID 목록'].append(i[0])
                    
            elif user_id in user_list['등록된 ID 목록']:
                message = '이미 등록된 ID입니다.'
            return render_template('index.html', message=message, user_list=user_list)
        
        # Remove ID
        elif request.form['choice'] == 'Remove ID':
            User_only.query.filter_by(user_id=user_id).delete()
            db.session.commit()
            
            user_list = {'등록된 ID 목록' : []}
            for i in User_only.query.with_entities(User_only.user_id).all():
                user_list['등록된 ID 목록'].append(i[0])
            
            message = f'{user_id}가 삭제되었습니다.'
            return render_template('index.html', message=message, user_list=user_list)
