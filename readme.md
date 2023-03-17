```
literacy    
    +--make_data    
        +--main    
            +--__init__.py    
            +--routes.py    
        +--models    
            +--database.py    
        +--templates    
            +--index.html   
            +--api_test.html
            +--decom.html
            +--db_test.html
        +--utils    
            +--__init__.py    
            +--kogpt.py
            +--chatgpt.py
        +--__init__.py    
        +--extensions.py    
    +--run.py    
    +--requirements.txt
```
수정하실 HTML : make_data -> templates -> decom.html
참고하실 DB : make_data -> models -> database.py
라우터 : make_data -> main -> routes.py -> @bp.route('/decom')