from make_web.main import kakao_bp

from flask import render_template, request, redirect, url_for

@kakao_bp.route('/', methods=['GET'])
def main():
    message = 'Hi'
    
    if request.method == 'POST':
        dialogue = request.files['file']
    
    return render_template('kakao/index.html', message=message)