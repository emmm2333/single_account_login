from flask import Flask
from settings import Config
from app.extensions import db, socketio, login_manager
from app.routes import demo_bp
from app.events import store_sid, verify_login_again


def create_app():
    app = Flask('SingleAccountLogin')
    app.config.from_object(Config)

    db.init_app(app)
    socketio.init_app(app)
    login_manager.init_app(app)

    app.register_blueprint(demo_bp)

    return app
