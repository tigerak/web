import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = \
        os.environ.get('DATABASE_URI')\
        or 'sqlite:///' + os.path.join(basedir, 'DB.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_CONTENT_LENGTH=1024*1024 # 1mb 이상 파일 업로드 금지