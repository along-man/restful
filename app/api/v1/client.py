"""
    created by along on 2025.03.18
    该模块用于处理客户端注册相关的API请求。
"""
from app.libs.enums import ClientTypeEnum
from app.libs.error_code import Success
from app.libs.redprint import Redprint
from app.models.user import User
from app.validators.forms import UserEmailForm, ClientForm

# 创建client红图
api = Redprint('client')


@api.route('/register', methods=['POST'])
def create_client():
    """
    客户端注册接口

    返回值:
    - 注册成功的响应
    """
    # 验证客户端表单数据
    form = ClientForm().validate_for_api()
    # 定义不同类型客户端的注册方法
    promise = {
        ClientTypeEnum.USER_EMAIL: __register_user_by_email
    }
    # 根据客户端类型调用相应的注册方法
    promise[form.type.data]()
    # 返回成功响应
    return Success()


def __register_user_by_email():
    """
    通过邮箱注册用户

    返回值:
    - 无
    """
    # 验证用户邮箱表单数据
    form = UserEmailForm().validate_for_api()
    # 调用用户模型的邮箱注册方法
    User.register_by_email(
        nickname=form.nickname.data,  # 用户昵称
        account=form.account.data,  # 用户账号
        secret=form.secret.data  # 用户密码
    )