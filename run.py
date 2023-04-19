from extensions import db, kakao_db
from config import Config

from flask import Flask

def create_app(config_class):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    from main import bp as main_bp
    app.register_blueprint(main_bp)

    from main import kakao_bp
    app.register_blueprint(kakao_bp)

    return app

app = create_app(Config)
    
if __name__=='__main__':
    
    with app.app_context():
        db.create_all()
        # kakao_db.create_all()
    app.run(host='0.0.0.0', port='5000')