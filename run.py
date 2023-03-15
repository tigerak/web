from make_data import create_app
from make_data.extensions import db
from config import Config

if __name__=='__main__':
    app = create_app(Config)
    with app.app_context():
        db.create_all()
    app.run(port='8000')
    