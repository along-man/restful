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

# 创建红图实例，用于定义API路由
api = Redprint('token')

# API登录 生成Token令牌
@api.route('', methods = ['POST'])
def get_token():
    """
    生成Token令牌的API接口

    返回值:
    - 返回生成的令牌，HTTP状态码为201
    """
    # form是通过验证后的表单对象
    form = ClientForm().validate_for_api()
    # 根据客户端类型选择验证方法
    promise = {
        ClientTypeEnum.USER_EMAIL: User.verify  # 邮箱登录,还有其他方式
    }
    # 验证用户身份
    identity = promise[form.type.data](
        form.account.data,
        form.secret.data,
    )
    # 生成令牌
    expiration = current_app.config['TOKEN_EXPIRATION']
    token = generate_auth_token(identity['uid'],
                                form.type.data,
                                identity['scope'],
                                expiration)
    # 返回生成的令牌
    t = {
        'token': token.decode('ascii')
    }
    return jsonify(t), 201

def generate_auth_token(uid, identity_type, scope,
                        expiration=7200):
    """
    生成令牌

    参数:
    - uid: 用户ID
    - identity_type: 身份类型
    - scope: 权限范围
    - expiration: 令牌过期时间，默认为7200秒

    返回值:
    - 返回生成的令牌字符串
    """
    # 使用SECRET_KEY和过期时间创建Serializer实例
    s = Serializer(current_app.config['SECRET_KEY'],
                   expires_in=expiration)
    # 将用户ID和身份类型写入令牌
    return s.dumps({
        'uid': uid,
        'type': identity_type.value,
        'scope': scope
    })