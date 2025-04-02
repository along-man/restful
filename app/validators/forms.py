from wtforms import IntegerField, StringField, ValidationError
from wtforms.validators import DataRequired, Length, Email, Regexp

from app.validators.base import BaseForm as Form
from app.libs.enums import ClientTypeEnum
from app.models.user import User


class ClientForm(Form):
    """
    客户端验证层的基类，用于验证客户端注册信息。
    """
    account = StringField(validators=[DataRequired(message='不允许为空'), Length(
        min=5, max=32
    )])
    secret = StringField()
    type = IntegerField(validators=[DataRequired()])

    # 验证客户端类型是否有效
    def validate_type(self, value):
        try:
            client = ClientTypeEnum(value.data)
        except ValueError as e:
            raise ValidationError(str(e))        # 错误信息存入 form.errors
            # raise ValidationError(e.args[0])   # 也可以
            # raise e                            # 还是会抛出异常

        self.type.data = client


class UserEmailForm(ClientForm):
    """验证邮箱注册的信息"""
    account = StringField(validators=[
        Email(message='invalidate email')
    ])
    secret = StringField(validators=[
        DataRequired(),
        # password can only contain letters, numbers and '_'
        Regexp(r'^[A-Za-z0-9_*&$#@]{6,22}$')
    ])
    nickname = StringField(validators=[DataRequired(),
                                        Length(min=2, max=22)])

    # 验证邮箱是否已经注册
    def validate_account(self, value):
        if User.query.filter_by(email=value.data).first():
            print("Email already registered")
            raise ValidationError("邮箱已注册")
        # try:
        #     User.query.filter_by(email=value.data).first()   
        # except ValueError as e:
        #     raise ValidationError(str(e))