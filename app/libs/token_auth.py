"""
    created by along on 2025.04.01

    token_auth.py 文件用于处理基于令牌的身份验证。
    主要功能包括：
    - 验证用户提供的令牌是否有效
    - 处理令牌过期或无效的情况
    - 在请求上下文中存储用户信息以便后续使用

    使用的技术栈：
    - Flask：Web框架
    - Flask-HTTPAuth：提供HTTP基本认证支持
    - itsdangerous：用于生成和验证签名令牌
"""

from flask import current_app, g  
from flask_httpauth import HTTPBasicAuth  
from itsdangerous import TimedJSONWebSignatureSerializer as\
    Serializer, BadSignature, SignatureExpired
from app.libs.error_code import AuthFailed  
from collections import namedtuple  # 用于创建简单的不可变对象

# 创建HTTP基本认证实例
auth = HTTPBasicAuth()

# 定义User命名元组，包含用户ID、认证类型和权限范围
User = namedtuple('User', ['uid', 'ac_type', 'scope'])

@auth.verify_password
def verify_password(token, password):
    """
    验证密码回调函数，实际只使用令牌进行身份验证。

    参数:
    - token: 用户提供的令牌
    - password: 保留参数，未使用

    返回值:
    - 如果令牌有效，返回True，并将用户信息存储在g.user中
    - 如果令牌无效或不存在，返回False
    """
    user_info = verify_auth_token(token)  # 验证令牌并获取用户信息
    if not user_info:
        return False
    else:
        g.user = user_info  # 将用户信息存储在g对象中
        return True

def verify_auth_token(token):
    """
    验证令牌的有效性和完整性。

    参数:
    - token: 用户提供的令牌字符串

    返回值:
    - 如果令牌有效，返回一个包含用户信息的User对象
    - 如果令牌无效或已过期，抛出相应的异常

    异常:
    - AuthFailed: 当令牌无效或已过期时抛出
    """
    s = Serializer(current_app.config['SECRET_KEY'])  # 创建序列化器，使用应用配置中的密钥
    try:
        data = s.loads(token)  # 解析令牌内容
    except BadSignature:
        raise AuthFailed(msg='token is invalid', error_code=1002)  # 令牌签名无效
    except SignatureExpired:
        raise AuthFailed(msg='token is expired', error_code=1003)  # 令牌已过期

    uid = data['uid']  # 从解析结果中提取用户ID
    ac_type = data['type']  # 从解析结果中提取认证类型
    return User(uid, ac_type, "")  # 返回包含用户信息的User对象