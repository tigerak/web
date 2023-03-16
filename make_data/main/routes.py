from make_data.main import bp
from make_data.utils import decomposition, SendToChatGPT
from make_data.models.database import Para_data, Sent_data, User_only
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
        para = request.form['decomp']
        para_input = Para_data(user_id, para)
        
        output_list = decomposition(para)
        for sent in output_list:
            for _, v in sent.items():
                sent_input = Sent_data(sent=v)
                sent_input.para_data = para_input
        db.session.add(sent_input)
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
        text = response.json()
        return render_template('api_test.html', 
                               user_id=user_id, 
                               db_items=db_items,
                               text=text)
        
    return render_template('api_test.html', user_id=user_id)

@bp.route('/api/feed/<user_id>', methods=['POST'])
def send_json(user_id):
    if request.method == 'POST':
        send = SendToChatGPT().make_data(user_id)
        return send


@bp.route('/db_test', methods=['GET', 'POST'])
def sql():
    P_items = Para_data.query.all()
    S_items = Sent_data.query.all()
    
    # 지문 삭제
    if request.form:
        del_num = request.form['delNum']
        
        Para_data.query.filter_by(id=del_num).delete()
        Sent_data.query.filter_by(p_id=del_num).delete()
        db.session.commit()
        
        P_items = Para_data.query.all()
        S_items = Sent_data.query.all()
        
    return render_template('db_test.html', P_items=P_items ,S_items=S_items)

