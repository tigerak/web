from make_data.main import bp
from make_data.utils import decomposition
from make_data.models.database import Para_data, Sent_data
from make_data.extensions import db
from config import Maum_api

from flask import render_template, request, redirect, url_for
import requests

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
    
@bp.route('/api', methods=['GET', 'POST'])
def api():
    import json
    prompt = "다음 글을 따라쓰면서 중요한 단어에는 별표시를 해줘. 그리고 한 문장으로 요약해줘. : "
    completion = "\n\n\n성소수자 등 성 문제에 대한 인식의 충돌도 이에 해당된다고 볼 수 있다. 최근 국내에서 주목받는 MZ세대의 정치적 지향의 변화에는, ‘정치적 올바름(PC)’에 대한 좌절과 반발이 녹아있다. 앞서 서술한 부동산 문제 등을 둘러싼 사회경제적 좌절과 함께, 민주화시대를 관통하며 작동해온 각종 PC에 대한 정서적 반발이 작동하고 있는 것이다."
    data = {
        "prompt" : prompt,
        "completion" : completion
    }
    send = json.dumps(data)
    return send

@bp.route('/feed', methods=['GET', 'POST'])
def get_json():
    ans = Maum_api.part
    response = requests.post(Maum_api.url, json=ans)
    text = response.json()
    return text

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