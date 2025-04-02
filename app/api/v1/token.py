"""
    created by along on 2025.03.31
    封装Token令牌相关接口,也就是登录接口
"""
from flask import current_app, jsonify
from app.libs.enums import ClientTypeEnum
from app.libs.redprint import Redprint
from app.models.user import User
from app.validators.forms import ClientForm
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

# 创建Redprint实例，用于定义API路由
api = Redprint('token')

# API登录 生成Token令牌
@api.route('', methods = ['POST'])
def get_token():
    # form是通过验证后的表单对象
    form = ClientForm().validate_for_api()
    # 根据客户端类型选择验证方法
    promise = {
        ClientTypeEnum.USER_EMAIL: User.verify  # 邮箱登录
    }
    # 验证用户身份
    identity = promise[form.type.data](
        form.account.data,
        form.secret.data
    )
    # 生成令牌
    expiration = current_app.config['TOKEN_EXPIRATION']
    token = generate_auth_token(identity['uid'],
                                form.type.data,
                                None,
                                expiration)
    # 返回生成的令牌
    t = {
        'token': token.decode('ascii')
    }
    return jsonify(t), 201

def generate_auth_token(uid, identity_type, scope=None,
                        expiration=7200):
    """生成令牌。Serializer.dumps将信息写入令牌中,返回字符串类型"""
    # 使用SECRET_KEY和过期时间创建Serializer实例
    s = Serializer(current_app.config['SECRET_KEY'],
                   expires_in=expiration)
    # 将用户ID和身份类型写入令牌
    return s.dumps({
        'uid': uid,
        'type': identity_type.value
    })