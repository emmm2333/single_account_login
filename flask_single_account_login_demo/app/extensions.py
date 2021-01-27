from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask_login import LoginManager
from flask import jsonify


db = SQLAlchemy()
socketio = SocketIO(cors_allowed_origins='*')
login_manager = LoginManager()


# 身份校验失败处理函数，重写扩展里面的
@login_manager.unauthorized_handler
def unauthorized():
    return jsonify({'code': 500, 'msg': u'请先登录'})