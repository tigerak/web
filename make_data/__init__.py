from make_data.init_db import init_database, db_session
from flask import Flask

app = Flask(__name__)
from make_data import views
from make_data.init_db import Base


# app.debug = True
# app.jinja_env.trim_blocks = True

app.config.update(
    SECRET_KEY='abc1234',
    SQLALCHEMY_DATABASE_URI = "sqlite+pysqlite:///:memory:",
    SQLALCHEMY_TRACK_MODIFICATIONS = False,
    MAX_CONTENT_LENGTH=1024*1024 # 1mb 이상 파일 업로드 금지
    
)

@app.before_first_request
def beforeFirstRequest():
    print('>> before_first_request !!')
    init_database(Base)

# @app.after_request
# def afterRequest():
#     print('>> after_request !!')
    
@app.teardown_request
def teardownRequest(exception):
    print('>> teardown_request !!', exception)
    
@app.teardown_appcontext
def teardownAppcontext(exception):
    print('>> teardown_appcontext !!', exception)
    db_session.remove()