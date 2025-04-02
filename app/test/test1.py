
from flask import Blueprint
from flask.json import jsonify, request

from app.libs.enums import ClientTypeEnum
from app.models.user import User
from app.validators.forms import ClientForm, UserEmailForm

api = Blueprint('api', __name__)

@api.route('/get')
def get():
    return 'Hello World!'

# 客户端注册接口
@api.route('/register', methods=['POST'])
def create_client():
    data = request.json
    print(f"Received data: {data}")  # 调试日志
    form = ClientForm(data=data)
    print(f"Form data: {form.data}")  # 调试日志
    
    # 验证表单
    if form.validate():
        print(f"Valid form with type: {form.type.data}")  # 调试日志
        promise = {
            ClientTypeEnum.USER_EMAIL: __register_user_by_email
        }
        promise[form.type.data]()

        return "success"
    
    print("Invalid form")  # 调试日志
    return jsonify({'code': 400, 'message': '表单验证失败', 'errors': form.errors})

def __register_user_by_email():
    form = UserEmailForm(data=request.json)
    if form.validate():
        User.register_by_email(
            nickname=form.nickname.data,
            account=form.account.data,
            secret=form.secret.data
        )