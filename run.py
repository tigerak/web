from make_web import create_app
from make_web.extensions import db, kakao_db
from config import Config

if __name__=='__main__':
    app = create_app(Config)
    with app.app_context():
        db.create_all()
        # kakao_db.create_all()
    app.run(port='8000')
    