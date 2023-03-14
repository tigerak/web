from make_data.main import bp
from make_data.utils import decomposition
from make_data.models.database import Para_data, Sent_data
from make_data.extensions import db

from flask import render_template, request, redirect, url_for

@bp.route('/', methods=['GET', 'POST'])
def decom_but():
    if request.form:
        json = '아직 안 지웠음'
        para = request.form['decomp']
        para_input = Para_data(para)
        
        output_list = decomposition(para)
        for sent in output_list:
            for _, v in sent.items():
                sent_input = Sent_data(sent=v)
                sent_input.para_data = para_input
        db.session.add(sent_input)
        db.session.commit()
        return render_template('index.html', output_list=output_list)

    else:
        return render_template('index.html')

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

@bp.route('/test')
def ch():
    db_items = Para_data.query.all()
    return render_template('test.html', db_items=db_items)