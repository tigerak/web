from make_data import app
from make_data.utils import decomposition

from flask import render_template, request


@app.route('/', methods=['GET', 'POST'])
def but():
    if request.form:
        for _, para in request.form.items():
            output_list = decomposition(para)
            return render_template('index.html', output_list=output_list)
    else:
        output_list = ['아직 없음']
        return render_template('index.html', output_list=output_list)
