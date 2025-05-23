from sqlalchemy import Column, Integer, SmallInteger, String
from werkzeug.security import generate_password_hash, check_password_hash
from .base import Base, db
from ..libs.error_code import AuthFailed


class User(Base):
    id = Column(Integer, primary_key=True) 
    email = Column(String(24), unique=True, nullable=False)
    nickname = Column(String(24), unique=True)
    auth = Column(SmallInteger, default=1)
    _password = Column('password', String(100))

    def keys(self):
        return ['id', 'email', 'nickname',  'auth']

    @property
    def password(self):
        return self._password
    
    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    @staticmethod
    def register_by_email(nickname, account, secret):
        """通过邮件创建一个对象"""
        with db.auto_commit():
            user = User()
            user.nickname = nickname
            user.email = account
            user.password = secret
            db.session.add(user)
            print(f"Adding user: {nickname}, {account}")  # 调试日志

    @staticmethod
    def verify(email, password):
        """验证用户邮箱登录的账号密码"""
        user = User.query.filter_by(email=email).first_or_404()
        if not user.check_password(password):
            raise AuthFailed()
        scope = 'SuperScope' if user.auth == 2 else 'UserScope'
        return {'uid': user.id, 'scope': scope}
    def check_password(self, raw):
        if not self._password:
            return False
        return check_password_hash(self._password, raw)
