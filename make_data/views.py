from make_data import app
from make_data.utils import decomposition
from make_data.models import para_data
from make_data.init_db import db_session

from flask import render_template, request


@app.route('/', methods=['GET', 'POST'])
def but():
    if request.form:
        for _, para in request.form.items():
            para_input = para_data(para)
            db_session.add(para_input)
            db_session.commit()
            output_list = decomposition(para)
            return render_template('index.html', output_list=output_list)
    else:
        output_list = [{'0_0' : '아직 없음'}]
        return render_template('index.html', output_list=output_list)
