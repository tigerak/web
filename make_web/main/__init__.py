from flask import Blueprint

bp = Blueprint('main', __name__,
               template_folder='literacy')
from make_web.main.literacy import routes

kakao_bp = Blueprint('kakao', __name__, 
                     url_prefix='/kakao',
                     template_folder='kakao')
from make_web.main.kakao import routes