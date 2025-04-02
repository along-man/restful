from app.libs.enums import ClientTypeEnum
from app.libs.error_code import Success
from app.libs.redprint import Redprint
from app.models.user import User
from app.validators.forms import UserEmailForm, ClientForm

# 创建client红图
api = Redprint('client')

# 客户端注册接口
@api.route('/register', methods=['POST'])
def create_client():
    form = ClientForm().validate_for_api()
    promise = {
        ClientTypeEnum.USER_EMAIL: __register_user_by_email
    }
    promise[form.type.data]()

    return Success()


# 通过邮箱注册
def __register_user_by_email():
    form = UserEmailForm().validate_for_api()
    User.register_by_email(
        nickname=form.nickname.data,
        account=form.account.data,
        secret=form.secret.data
    )
            
