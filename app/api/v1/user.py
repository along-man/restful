"""
    created by along on 2025.03.18
"""
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.models.user import User

# 创建user红图
api = Redprint('user')

@api.route('/<int:uid>', methods=['POST'])
@auth.login_required
def get_user(uid):
    user = User.query.get_or_404(uid)
    return 'get user'

