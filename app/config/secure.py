"""
    created by along on 2025.03.18
    配置文件，包含数据库连接信息和密钥配置
"""
# 数据库连接URI，使用MySQL数据库
SQLALCHEMY_DATABASE_URI = \
    'mysql+pymysql://root:123456@localhost:3307/ginger'
# 是否追踪数据库修改，设置为False以提高性能
SQLALCHEMY_TRACK_MODIFICATIONS = False
# 用于加密的密钥
SECRET_KEY = '123456'