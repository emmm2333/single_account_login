from flask import Blueprint, request, render_template, jsonify, session
from flask_login import login_user, login_required
from app.models import User
from app.extensions import db
from app.utils import verify_token
from app.events import verify_login_again
import random


demo_bp = Blueprint('demo', __name__)


@demo_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    username = request.json.get('username')
    password = request.json.get('password')
    user_obj = User.query.filter_by(username=username, password=password).first()

    if not user_obj:
        return jsonify({'code': 500, 'msg': '账号或者密码有误'})

    # 更新 user_obj的auth_session_token，并且将新的token写入session
    new_token = '%064x' % random.getrandbits(255)
    user_obj.single_account_login_token = new_token
    db.session.commit()

    verify_login_again(user_obj)

    login_user(user_obj)
    session['token'] = new_token
    return jsonify({'code': 200, 'msg': '登录成功'})


@demo_bp.route('/other_page')
@login_required
@verify_token
def other_page():
    return render_template('other_page.html')


@demo_bp.route('/bar')
@login_required
@verify_token
def bar():
    return 'bar'


@demo_bp.route('/foo')
@login_required
@verify_token
def foo():
    return 'foo'
