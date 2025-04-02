"""
    created by along on 2025.03.18
"""

from flask import Blueprint
from app.api.v1 import book, user, client, token


def create_blueprint_v1():
    # 创建v1蓝图
    bp_v1 = Blueprint('v1', __name__)
    # 注册红图到v1
    book.api.register(bp_v1)
    user.api.register(bp_v1)
    client.api.register(bp_v1)
    token.api.register(bp_v1)
    return bp_v1
