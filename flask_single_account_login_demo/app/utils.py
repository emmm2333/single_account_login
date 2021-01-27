from flask import session, jsonify
from flask_login import current_user
from flask_socketio import emit
from functools import wraps
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


def verify_token(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        session_token = session.get('token')
        if session_token != current_user.single_account_login_token:
            return jsonify({'code': 500, 'msg': '登录已失效'})

        return f(*args, **kwargs)

    return wrapper


def access_after_login(event_name):
    """
    socketio事件装饰器
    """
    def authenticated_only(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated:
                emit(event_name, {'code': 500, 'msg': '请先登录'})
                return False
            else:
                return f(*args, **kwargs)

        return wrapper

    return authenticated_only
