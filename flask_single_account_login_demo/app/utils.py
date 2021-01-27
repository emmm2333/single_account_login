from flask_login import current_user
from app.extensions import socketio
from functools import wraps
from datetime import datetime
import redis


class SingletonRedis(object):
    def __init__(self, *args, **kwargs):
        ...

    @classmethod
    def connection(cls):
        if not hasattr(SingletonRedis, '_instance'):
            SingletonRedis._instance = redis.Redis(
                host='127.0.0.1',
                port=6379,
                db=1,
                password=None,
                decode_responses=True)

        return SingletonRedis._instance


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
    socketio.emit('verify_login_resp', {'code': 403, 'msg': msg}, room=current_user_sid, namespace='/')
    return True


def access_after_login(event_name):
    """
    socketio事件装饰器
    """
    def authenticated_only(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated:
                socketio.emit(event_name, {'code': 500, 'msg': '请先登录'})
                return False
            else:
                return f(*args, **kwargs)

        return wrapper

    return authenticated_only
