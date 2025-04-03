"""
    created by along on 2025.04.03
    这是一个用于创建测试用户的脚本
"""
from app import create_app
from app.models.base import db
from app.models.user import User

# 创建Flask应用实例
app = create_app()

# 在应用上下文中执行数据库操作
with app.app_context():
    # 使用自动提交事务
    with db.auto_commit():
        user = User()
        user.nickname = 'Super'  # 设置用户昵称
        user.password = '123456'  # 设置用户密码
        user.email = '999@qq.com'  # 设置用户邮箱
        user.auth = 2  # 设置用户权限级别
        db.session.add(user)  # 将用户添加到数据库会话