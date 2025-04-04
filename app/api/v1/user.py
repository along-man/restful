"""
    created by along on 2025.03.18
    该模块用于处理用户相关的API请求，包括获取用户信息和删除用户。
"""
from flask import jsonify, g
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.libs.error_code import DeleteSuccess, AuthFailed
from app.models.base import db
from app.models.user import User

# 创建user红图
api = Redprint('user')


@api.route('/<int:uid>', methods=['GET'])
@auth.login_required
def super_get_user(uid):
    """
    获取指定用户信息（需管理员权限）

    参数:
    - uid: 用户ID

    返回值:
    - 用户信息的JSON格式数据
    """
    user = User.query.filter_by(id=uid).first_or_404()
    return jsonify(user)


@api.route('', methods=['GET'])
@auth.login_required
def get_user():
    """
    获取当前登录用户信息

    返回值:
    - 用户信息的JSON格式数据
    """
    uid = g.user.uid
    user = User.query.filter_by(id=uid).first_or_404()
    return jsonify(user)


@api.route('', methods=['DELETE'])
@auth.login_required
def delete_user():
    """
    删除当前登录用户

    返回值:
    - 删除成功的响应
    """
    uid = g.user.uid
    with db.auto_commit():
        user = User.query.filter_by(id=uid).first_or_404()
        user.delete()
    return DeleteSuccess()