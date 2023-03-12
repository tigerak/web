from flask import Blueprint

bp = Blueprint('main', __name__)

from make_data.main import routes