"""
    created by along on 2025.03.18
"""
from app.libs.redprint import Redprint

# 创建book红图
api = Redprint('book')

@api.route('/get')
def get_book():
    return 'Hello World!'