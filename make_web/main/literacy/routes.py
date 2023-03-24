from make_web.main import bp
from make_web.extensions import db
from make_web.models import Text_data, Sent_data, Point_data, Key_data, User_only
from make_web.utils import sign, decomposition, SendToChatGPT, ChatGPT
from config import Maum_api

from flask import render_template, request, redirect, url_for

@bp.route('/', methods=['GET', 'POST'])
def login():
    message = 'ID를 입력해주세요'
    
    if request.method == 'POST':
        render = sign(request.form)
        return render

    return render_template('literacy/index.html', message=message)

@bp.route('/decom', methods=['GET', 'POST'])
def decom_but():
    user_id = 'loader'
    output_list = []
    if request.method == 'POST':
        if 'decomp' in request.form.keys():
            text = request.form['decomp']
            # text_input = Text_data(user_id, text)
            
            sent_list, output_list = decomposition(text)
            
            # Sent DB Save
            # for sent in sent_list:
            #     sent_input = Sent_data(sent=sent)
            #     sent_input.text_data = text_input
                
            #     for s in output_list:
            #         for k, v in s.items():
            #             key_input = Key_data(key=v)
            #             key_input.sent_data = sent_input
            #         for k in text[:10]:
            #             key_input = Key_data(key=k)
            #             key_input.point_data = point_input
                
            # db.session.add(sent_input)
            # db.session.commit()
            return render_template('literacy/decom.html', 
                                output_list=output_list)
            
        elif 'key' in request.form.keys():
            sent_list = request.form
            return render_template('literacy/decom.html', 
                                output_list=output_list,
                                sent_list=sent_list)
            
        else:
            sent_list = request.form
            return render_template('literacy/decom.html', 
                                output_list=output_list,
                                sent_list=sent_list)
        

    else:
        return render_template('literacy/decom.html')
    
@bp.route('/sentence', methods=['POST'])
def sentence():
    if request.method == 'POST':
        md = request.form
        return render_template('literacy/decom.html',
                               sent_list=md)


from sqlalchemy import desc
@bp.route('/api/<user_id>', methods=['GET', 'POST'])
def api(user_id):
    db_items = User_only.query.order_by(desc(User_only.date)).limit(1)
    
    if request.method == 'POST':
        query = request.form
        
        # Maum API -> False : Can't send activating address
        SendToChatGPT().save_db(user_id, query)
        db_items = User_only.query.filter_by(user_id=user_id).all()
        
        response = Maum_api(user_id).doc()
        text = response.json()
        
        # openAI chatGPT API -> OK!
        # text = ChatGPT().ping(query)
        
        return render_template('literacy/api_test.html', 
                               user_id=user_id, 
                               db_items=db_items,
                               text=text)
        
    return render_template('literacy/api_test.html', user_id=user_id, 
                               db_items=db_items)

@bp.route('/api/feed', methods=['POST'])
def send_json():
    if request.method == 'POST':
        send = SendToChatGPT().make_data()
        return send


@bp.route('/db_test', methods=['GET', 'POST'])
def sql():
    T_items = Text_data.query.all()
    S_items = Sent_data.query.all()
    P_items = Point_data.query.all()
    K_items = Key_data.query.all()
    
    # 지문 삭제
    if request.form:
        del_num = request.form['delNum']
        
        Text_data.query.filter_by(id=del_num).delete()
        Sent_data.query.filter_by(t_id=del_num).delete()
        Point_data.query.filter_by(t_id=del_num).delete()
        Key_data.query.filter_by(t_id=del_num).delete()
        db.session.commit()
        
        T_items = Text_data.query.all()
        S_items = Sent_data.query.all()
        P_items = Point_data.query.all()
        K_items = Key_data.query.all()
        
    return render_template('literacy/db_test.html', 
                           T_items=T_items, 
                           P_items=P_items,
                           S_items=S_items,
                           K_items=K_items)

