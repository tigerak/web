```
literacy    
    +--make_web
        +--__init__.py
        +--extensions.py
        +--main
            +--__init__.py
            +--kakao
                +--routes.py
            +--literacy
                +--routes.py    
        +--models
            +--__init__.py
            +--literacy
                +--database.py
        +--templates
            +--kakao
                +--index.html
            +--literacy
                +--index.html   
                +--api_test.html
                +--decom.html
                +--db_test.html
        +--utils
            +--__init__.py
            +--login.py
            +--kakao
                +--__init__.py
                +--bert_utile.py
            +--literacy
                +--__init__.py
                +--kogpt.py
                +--chatgpt.py
    +--run.py    
    +--requirements.txt
```
수정하실 HTML : make_web -> templates -> literacy -> decom.html<br>
참고하실 DB : make_web -> models -> literacy -> database.py<br>
라우터 : make_web -> main -> literacy -> routes.py -> @bp.route('/decom')