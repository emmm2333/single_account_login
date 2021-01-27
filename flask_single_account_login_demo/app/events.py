from flask import request
from flask_login import current_user
from flask_socketio import emit
from app.extensions import socketio
from app.utils import SingletonRedis, access_after_login
from datetime import datetime


@socketio.on('store_sid')
@access_after_login('store_sid_resp')
def store_sid():
    r = SingletonRedis.connection()
    r.hset('current_user_sid', current_user.id, request.sid)
    emit('store_sid_resp', {'code': 200, 'msg': '存储sid成功'})


@socketio.on('verify_login_again')
@access_after_login('verify_login_resp')
def verify_login_again(user_obj):
    """
    验证是否是二次登录
    :return:
    """
    r = SingletonRedis.connection()
    current_user_sid = r.hget('current_user_sid', user_obj.id)
    if not current_user_sid:
        return False

    # 通知对方下线，sid为原设备的
    current_time = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
    msg = '当前账号于 {} 在另一台设备上登录。此客户端已退出登录'.format(current_time)
    emit('verify_login_resp', {'code': 403, 'msg': msg}, room=current_user_sid, namespace='/')
    return True
