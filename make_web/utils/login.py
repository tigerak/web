from make_web.models.literacy.database import User_only
from make_web.extensions import db

from flask import render_template, request, redirect

def sign(post_form):
        # Get User ID
        user_id = post_form['user_id']
        # User list
        user_list = {'등록된 ID 목록' : []}
        for i in User_only.query.with_entities(User_only.user_id).all():
            user_list['등록된 ID 목록'].append(i[0])
            
        # Sign in
        if post_form['choice'] == 'Sign in':
        
            if user_id == '':
                message = 'ID를 입력하지 않았습니다.'
                return render_template('literacy/index.html', message=message, user_list=user_list)
            
            elif user_id not in user_list['등록된 ID 목록']:
                message = '없는 ID 입니다.'
                return render_template('literacy/index.html', message=message, user_list=user_list)
            
            elif user_id in user_list['등록된 ID 목록']:
                return redirect(f'/api/{user_id}')
            
        # Sign UP
        elif request.form['choice'] == 'Sign up':
            
            if user_id not in user_list['등록된 ID 목록']:
                send_api_data = User_only(user_id, 'prompt', 'completion')
                db.session.add(send_api_data)
                db.session.commit()
                
                message = 'ID가 등록되었습니다. \nSign in 해주세요.'
                
                user_list = {'등록된 ID 목록' : []}
                for i in User_only.query.with_entities(User_only.user_id).all():
                    user_list['등록된 ID 목록'].append(i[0])
                    
            elif user_id in user_list['등록된 ID 목록']:
                message = '이미 등록된 ID입니다.'
            return render_template('literacy/index.html', message=message, user_list=user_list)
        
        # Remove ID
        elif request.form['choice'] == 'Remove ID':
            User_only.query.filter_by(user_id=user_id).delete()
            db.session.commit()
            
            user_list = {'등록된 ID 목록' : []}
            for i in User_only.query.with_entities(User_only.user_id).all():
                user_list['등록된 ID 목록'].append(i[0])
            
            message = f'{user_id}가 삭제되었습니다.'
            return render_template('literacy/index.html', message=message, user_list=user_list)
