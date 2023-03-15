import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = \
        os.environ.get('DATABASE_URI')\
        or 'sqlite:///' + os.path.join(basedir, 'test_DB.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_CONTENT_LENGTH=1024*1024 
    
class Maum_api:
    part = {
        "app_id": "83fdc22a-20d1-5fc8-8af8-a6efe6b4af69",
        "name": "문해력",
        "item": [
            "open-api-get-query"
        ],
        "param": [
            "https://e4e7-14-36-34-28.jp.ngrok.io/api"
        ]
    }