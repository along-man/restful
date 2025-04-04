"""
    created by along on 2025.04.04
    该模块用于定义不同用户角色的权限范围。
    每个类代表一个用户角色，并定义该角色允许访问的API端点。
"""
class Scope:
    # 允许访问的API端点列表
    allow_api = []
    
    # 重载加法运算符，用于合并不同角色的权限
    def __add__(self, other):
        self.allow_api = other.allow_api + self.allow_api
        self.allow_api = list(set(self.allow_api))  # 去重
        return self

class UserScope(Scope):
    """
    普通用户角色，拥有基本权限。
    允许访问的API端点包括：
    - v1.get_token: 获取令牌
    - v1.get_user: 获取用户信息
    - v1.create_client: 创建客户端
    """
    allow_api = ['v1.get_token', 'v1.get_user', 'v1.create_client']

class AdminScope(Scope):
    """
    管理员角色，拥有较高的权限。
    允许访问的API端点包括：
    - get_user: 获取用户信息
    - delete_user: 删除用户
    """
    allow_api = ['get_user', 'delete_user']
    
    def __init__(self):
        # 继承UserScope的权限
        self + UserScope()

class SuperScope(Scope):
    """
    超级管理员角色，拥有最高权限。
    允许访问的API端点包括：
    - v1.super_get_user: 获取用户信息（超级管理员权限）
    """
    allow_api = ['v1.super_get_user']
    
    def __init__(self):
        # 继承AdminScope和UserScope的权限
        self + AdminScope() + UserScope()

def is_in_scope(scope, endpoint):
    """
    检查给定的API端点是否在指定角色的权限范围内。

    参数:
    - scope: 用户角色实例
    - endpoint: 要检查的API端点

    返回值:
    - 如果端点在该角色的权限范围内，返回True；否则返回False
    """
    scope = globals()[scope]()  # 根据角色名称获取角色实例
    if endpoint in scope.allow_api:
        return True
    return False
