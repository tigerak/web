from make_data.main import bp
from make_data.utils import decomposition, SendToChatGPT
from make_data.models.database import Text_data, Sent_data, Point_data, Key_data, User_only
from make_data.extensions import db
from config import Maum_api

from flask import render_template, request, redirect, url_for
import requests
import json

@bp.route('/', methods=['GET', 'POST'])
def login():
    message = 'ID를 입력해주세요'
    
    if request.method == 'POST':
        user_list = []
        for i in User_only.query.with_entities(User_only.user_id).all():
            user_list.append(i[0])
    
        user_id = request.form['user_id']
    
        if user_id is '':
            message = 'ID를 입력하지 않았습니다.'
            return render_template('index.html', message=message)
        
        elif user_id not in user_list:
            message = '없는 ID 입니다.'
            return render_template('index.html', message=message)
        
        elif user_id in user_list:
            return redirect(f'/api/{user_id}')
        
    return render_template('index.html', message=message)

@bp.route('/decom', methods=['GET', 'POST'])
def decom_but():
    user_id = 'loader'
    
    if request.method == 'POST':
        text = request.form['decomp']
        text_input = Text_data(user_id, text)
        
        sent_list, output_list = decomposition(text)
        
        # Sent DB Save
        for sent in sent_list:
            sent_input = Sent_data(sent=sent)
            sent_input.text_data = text_input
            
        for w in output_list:
            for _, m in w.items():
                point_input = Point_data(point=m)
                point_input.text_data = text_input
                for k in text[:10]:
                    key_input = Key_data(key=k)
                    key_input.point_data = point_input
            
        db.session.add(key_input)
        db.session.commit()
        return render_template('decom.html', output_list=output_list)

    else:
        return render_template('decom.html')

@bp.route('/api/<user_id>', methods=['GET', 'POST'])
def api(user_id):
    # user_id = 'loader'
    
    if request.form:
        query = request.form
        SendToChatGPT().save_db(user_id, query)
        db_items = User_only.query.filter_by(user_id=user_id).all()
        
        maum_url, data = Maum_api(user_id).doc()
        response = requests.post(maum_url, json=data)
        # text = response.json()
        return render_template('api_test.html', 
                               user_id=user_id, 
                               db_items=db_items,
                               text=response,
                               send=data)
        
    return render_template('api_test.html', user_id=user_id)

@bp.route('/api/feed/<user_id>', methods=['GET', 'POST'])
def send_json(user_id):
    if request.method == 'POST':
        send = SendToChatGPT().make_data(user_id)
        return send


@bp.route('/db_test', methods=['GET', 'POST'])
def sql():
    T_items = Text_data.query.all()
    P_items = Point_data.query.all()
    K_items = Key_data.query.all()
    
    # 지문 삭제
    if request.form:
        del_num = request.form['delNum']
        
        Text_data.query.filter_by(id=del_num).delete()
        Point_data.query.filter_by(t_id=del_num).delete()
        Key_data.query.filter_by(p_id=del_num).delete()
        db.session.commit()
        
        T_items = Text_data.query.all()
        P_items = Point_data.query.all()
        K_items = Key_data.query.all()
        
    return render_template('db_test.html', T_items=T_items, P_items=P_items ,S_items=K_items)

