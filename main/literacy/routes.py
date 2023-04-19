from main import bp
from extensions import db
from models import Text_data, Sent_data, Point_data, Key_data, User_only
from utils import (sign, decomposition, classification, DB_edit,
                    SendToChatGPT, ChatGPT)
# from config import Maum_api

from flask import render_template, request, redirect, url_for
from sqlalchemy import desc, and_


@bp.route('/', methods=['GET', 'POST'])
def login():
    message = 'ID를 입력해주세요'
    
    if request.method == 'POST':
        render = sign(request.form)
        return render

    return render_template('literacy/index.html', message=message)

@bp.route('/decom/<user_id>', methods=['GET', 'POST'])
def decom_but(user_id):
    
    if request.method == 'POST':
        if 'decomp' in request.form.keys():
            text_value = request.form['decomp']
            text_input = Text_data(user_id, text_value)
            
            sent_dict = decomposition(text_value)
            
            # Sent DB Save
            for i, sent in sent_dict.items():
                sent_input = Sent_data(s_id=i, sent=sent)
                sent_input.text_data = text_input
                
            db.session.add(sent_input)
            db.session.commit()
            
            return render_template('literacy/decom.html',
                                   user_id=user_id,
                                   t_id=text_input,
                                   sent_dict=sent_dict)
        
    else:
        return render_template('literacy/decom.html',
                               user_id=user_id)
    
    
@bp.route('/sentence/<user_id>', methods=['POST'])
def sentence(user_id):
    
    if request.method == 'POST':
        
        t_id, s_id, key_list, point_list = classification(request.form)
        
        for key_word in key_list:
            key_input = Key_data(user_id, t_id, s_id, key_word)
            for point_word in point_list:
                point_input = Point_data(point_word)
                point_input.key_data = key_input
                
            db.session.add(point_input)
            db.session.commit()
            
        K_items = Key_data.query.filter(and_(Key_data.t_id==t_id, Key_data.s_id==s_id)).\
                                 order_by(desc(Key_data.id)).all()
        P_items = Point_data.query.join(Key_data, Key_data.id==Point_data.k_id).\
                                   filter(and_(Key_data.t_id==t_id, Key_data.s_id==s_id)).\
                                   order_by(desc(Point_data.id)).all()

        return render_template('literacy/sub_db.html',
                                user_id=user_id,
                                K_items=K_items,
                                P_items=P_items)


@bp.route('/api', methods=['GET', 'POST'])
def api():
    if request.method == 'POST':
        query = request.form
        # Maum API -> False : Can't send activating address
        # SendToChatGPT().save_db(user_id, query)
        # db_items = User_only.query.filter_by(user_id=user_id).all()
        
        # response = Maum_api(user_id).doc()
        # text = response.json()
        
        # openAI chatGPT API -> OK!
        text = ChatGPT().ping(query)
        
        return render_template('literacy/api_test.html', 
                               text=text)
        
    return render_template('literacy/api_test.html')

# @bp.route('/api/feed', methods=['POST'])
# def send_json():
#     if request.method == 'POST':
#         send = SendToChatGPT().make_data()
#         return send


@bp.route('/db_check/<user_id>', methods=['GET', 'POST'])
def edit_sql(user_id):
    title = f'###### {user_id}님의 작업 현황 ######'

    # t_id 수집
    user_T = Text_data.query.filter_by(user_id=user_id).all()
    t_id_list = []
    for i in user_T:
        t_id_list.append(str(i))

    total_text_num = len(t_id_list)
    p_t_num = 1

    T_items, S_items, K_items, P_items = DB_edit().db_search(t_id_list,
                                                             p_t_num)
    
    # 지문 삭제
    if request.form:
        form_key_list = request.form.keys()

        if request.form['delNum'] != '':
            del_text = int(request.form['delNum'])
            DB_edit().delete_text(del_text)
        
        if request.form['delKey'] != '':
            del_key = int(request.form['delKey'])
            DB_edit().delete_key(del_key)
            
        if 'next' in form_key_list:
            num = int(request.form['next']) + 1
            p_t_num = DB_edit().check_p_t(num, total_text_num)
                                       
        if 'back' in form_key_list:
            num = int(request.form['back']) - 1
            p_t_num = DB_edit().check_p_t(num, total_text_num)

        if request.form['moveNum'] != '':
            num = int(request.form['moveNum'])
            p_t_num = DB_edit().check_p_t(num, total_text_num)
            
        T_items, S_items, K_items, P_items = DB_edit().db_search(t_id_list, 
                                                                 p_t_num)
          
    return render_template('literacy/db_check.html',
                           user_id=user_id,
                           title=title,
                           total_text=total_text_num,
                           p_t_num=p_t_num,
                           p_t_id=T_items,
                           T_items=T_items,
                           S_items=S_items,
                           K_items=K_items,
                           P_items=P_items)


@bp.route('/test', methods=['GET', 'POST'])
def test():
    test = request.form

    return render_template('literacy/test.html',
                           test=test)