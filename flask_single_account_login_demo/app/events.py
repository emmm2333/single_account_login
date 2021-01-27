from flask import request
from flask_login import current_user
from flask_socketio import emit
from app.extensions import socketio
from app.utils import SingletonRedis, access_after_login


@socketio.on('store_sid')
@access_after_login('store_sid_resp')
def store_sid():
    r = SingletonRedis.connection()
    r.hset('current_user_sid', current_user.id, request.sid)
    emit('store_sid_resp', {'code': 200, 'msg': '存储sid成功'})

