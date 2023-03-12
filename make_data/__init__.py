from make_data.extensions import db

from flask import Flask

def create_app(config_class):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)
    
    from make_data.main import bp as main_bp
    app.register_blueprint(main_bp)

    return app



# @app.before_first_request
# def beforeFirstRequest():
#     print('>> before_first_request !!')
#     init_database(Base)

# @app.after_request
# def afterRequest():
#     print('>> after_request !!')
    
# @app.teardown_request
# def teardownRequest(exception):
#     print('>> teardown_request !!', exception)
    
# @app.teardown_appcontext
# def teardownAppcontext(exception):
#     print('>> teardown_appcontext !!', exception)
#     db_session.remove()