from make_data.main import bp
from make_data.utils import decomposition
from make_data.models.database import Para_data, Sent_data
from make_data.extensions import db

from flask import render_template, request

@bp.route('/', methods=['GET', 'POST'])
def decom_but():
    if request.form:
        if request.form['paragraph']:
            for _, para in request.form.items():
                para_input = Para_data(para)
                db.session.add(para_input)
                
                output_list = decomposition(para)
                m = []
                for sent in output_list:
                    for _, v in sent.items():
                        sent_input = Sent_data(sent=v)
                        m.append(sent_input)
                        
                db.session.add_all(m)
                db.session.commit()
                return render_template('index.html', output_list=output_list, m=m)
    else:
        output_list = [{'0_0' : '아직 없음'}]
        return render_template('index.html', output_list=output_list)

@bp.route('/db_test')
def sql():
    db_items = Sent_data.query.all()
    
    return render_template('db_test.html', db_items=db_items)

@bp.route('/test')
def ch():
    db_items = Para_data.query.all()
    if request.form:
        if request.form['db_remove']:
            db.session.remove()
    return render_template('db_test.html', db_items=db_items)